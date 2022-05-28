import json
import logging
import os

import click
import torch
import tqdm
from transformers import AutoModel, AutoTokenizer

# from configuration import BATCH_SIZE, BERT_NAME, EMBEDDING_DIMENTION
from model.model import BiEncoder
from dataloader.utils import load_jsonl

logger = logging.getLogger(__name__)
logging.basicConfig(filename="../logs/create_embedding_matrix.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO
                    )

@click.command()
@click.option(
    "--domain_path",
    type=str,
    required=True,
)
@click.option(
    "--bert_name",
    type=str,
    required=True,
)
@click.option(
    "--embedding_dim",
    type=int,
    required=True,
)
@click.option(
    "--batch_size",
    type=int,
    required=False,
    default=32
)
@click.option(
    "--model_path",
    type=str,
    required=True
)
@click.option(
    "--output",
    type=str,
    required=True
)
def main(
    domain_path,
    bert_name,
    embedding_dim,
    batch_size,
    model_path,
    output
):            
    collection_file = os.path.join(domain_path, 'collection.jsonl')
    logging.debug(f'Loading collection file {collection_file}')
    data = load_jsonl(collection_file)
    corpus = {d['id']: d['title'] for d in tqdm.tqdm(data)}

    embedding_matrix = torch.zeros(len(corpus), embedding_dim).float()
    logging.info(f'Embedding Matrix dimentions: {embedding_matrix.shape}')

    logging.debug('Loading model and tokenizer')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = AutoTokenizer.from_pretrained(bert_name)
    query_model = AutoModel.from_pretrained(bert_name)
    doc_model = AutoModel.from_pretrained(bert_name)
    model = BiEncoder(query_model, doc_model, tokenizer, device)
    logging.info(f'Loading model at path {model_path}')
    model.load_state_dict(torch.load(model_path))

    index = 0
    batch_val = 0
    texts = []
    id_to_index = {}
    for id_, val in tqdm.tqdm(corpus.items()):
        id_to_index[id_] = index
        batch_val += 1
        index += 1
        texts.append(val)
        if batch_val == batch_size:
            with torch.no_grad():
                embedding_matrix[index - batch_val : index] = model.doc_encoder(texts).to('cpu')
            batch_val = 0
            texts = []

    if texts:
        embedding_matrix[index - batch_val : index, :] = model.doc_encoder(texts)


    os.makedirs(output, exist_ok=True)
    logging.info(f'Embedded {index} documents. Saving embedding matrix in folder {output}.')
    torch.save(embedding_matrix, os.path.join(output, 'collection_embedding.pt'))

    logging.info(f'Embedded {index} documents. Saving id_to_index.json in folder {output}.')
    with open(os.path.join(output, 'id_to_index.json'), 'w') as f:
        json.dump(id_to_index, f)


if __name__ == '__main__':
    main()