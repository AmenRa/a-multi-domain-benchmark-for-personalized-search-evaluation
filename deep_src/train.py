import logging
import os

import click
import numpy as np
import torch
import tqdm
from torch.optim import Adam
from torch.optim.lr_scheduler import StepLR
from transformers import AutoModel, AutoTokenizer

from dataloader.dataloader import TripletData
from dataloader.utils import load_jsonl, load_query_data, seed_everything
from model.model import BiEncoder, TripletMarginLoss

logger = logging.getLogger(__name__)

@click.command()
@click.option(
    "--domain_path",
    type=str,
    required=True,
)
@click.option(
    "--n_epochs",
    type=int,
    required=True
)
@click.option(
    "--batch_size",
    type=int,
    required=True,
)
@click.option(
    "--lr",
    type=float,
    required=False,
    default='5e-5',
    help='learning rate used for training'
)
@click.option(
    "--bert_name",
    type=str,
    required=True,
    help='BERT model name from hugging face repository'
)
@click.option(
    "--scheduler_step",
    type=int,
    required=False,
    help='number of step used by scheduler to reduce lr (-1 = no scheduling)',
    default=-1
)
@click.option(
    "--scheduler_gamma",
    type=float,
    required=False,
    help='gamma multiplicative value for scheduler',
    default=1
)
@click.option(
    "--output_folder",
    type=str,
    required=False,
    default='./saved_models'
)
@click.option(
    "--pretrained_weights",
    type=str,
    required=False,
    help='pretrained weights for the model specified with bert_name, useful for continue training'
)
@click.option(
    "--seed",
    type=int,
    required=False,
    help='random seed for reproducibility'
)
def main(
    domain_path,
    n_epochs,
    batch_size,
    lr,
    bert_name,
    scheduler_step,
    scheduler_gamma,
    output_folder,
    pretrained_weights,
    seed
):
    logging_file = f"training_{domain_path.split('/')[-1]}.log"
    logging.basicConfig(filename=os.path.join('../logs', logging_file),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO
                        )
    if seed:
        seed_everything(seed)
    collection = load_jsonl(os.path.join(domain_path, 'collection.jsonl'))
    corpus = {d['id']: d['title'] for d in tqdm.tqdm(collection, desc='Loading Collection Data')}

    logger.debug('Getting Tokenized and Models')
    tokenizer = AutoTokenizer.from_pretrained(bert_name)
    query_model = AutoModel.from_pretrained(bert_name)
    doc_model = AutoModel.from_pretrained(bert_name)

    logger.debug('Loading trainng and validation data')
    train_data = load_query_data(os.path.join(domain_path, 'train/queries.jsonl'))
    val_data = load_query_data(os.path.join(domain_path, 'val/queries.jsonl'))

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    loss_fn = TripletMarginLoss(0.1).to(device)
    model = BiEncoder(query_model, doc_model, tokenizer, device)
    optimizer = Adam(model.parameters(), lr=lr)
    if scheduler_step == -1:
        scheduler_step = n_epochs + 1 # this it is always higher than number of epoch and thus never decays 
    scheduler = StepLR(optimizer, step_size=scheduler_step, gamma=scheduler_gamma, verbose=False)
    
    if pretrained_weights:
        logger.info(f'Loading specified weights at {pretrained_weights}')
        model.load_state_dict(torch.load(pretrained_weights))
    
    os.makedirs(output_folder, exist_ok='true')

    logger.info('TRAINING INITIALIZED')
    for epoch in tqdm.tqdm(range(1, n_epochs+1)):
        train_dataset = TripletData(train_data, corpus)
        train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size)
        losses = []
        pbar = tqdm.tqdm(train_dataloader, total=len(train_dataloader), desc='Training')
        for triple in pbar:
            query_embedding, pos_embedding, neg_embedding = model(triple)
            
            optimizer.zero_grad()
            loss_val = loss_fn(query_embedding, pos_embedding, neg_embedding)
            loss_val.backward()
            optimizer.step()

            losses.append(loss_val.cpu().detach().item())
            average_loss = np.mean(losses)
            pbar.set_description("TRAIN EPOCH {:3d} Current loss {:.2e}, Average {:.2e}".format(epoch, loss_val, average_loss))

        model_name = os.path.join(output_folder, f"model_{epoch}.pt")
        torch.save(model.state_dict(), model_name)
        logger.info(f'EPOCH: {epoch}, Average Training Loss: {average_loss}')
        val_dataset = TripletData(val_data, corpus)
        val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size)
        losses = []
        pbar = tqdm.tqdm(val_dataloader, total=len(val_dataloader), desc='Validating')
        for triple in pbar:
            with torch.no_grad():
                query_embedding, pos_embedding, neg_embedding = model(triple)
                loss_val = loss_fn(query_embedding, pos_embedding, neg_embedding)
                losses.append(loss_val.cpu().detach().item())
            average_loss = np.mean(losses)
            pbar.set_description("VAL EPOCH {:3d} Current loss {:.2e}, Average {:.2e}".format(epoch, loss_val, average_loss))
        
        logger.info(f'EPOCH: {epoch}, Average Validation Loss: {average_loss}')
        scheduler.step()

if __name__ == '__main__':
    main()
