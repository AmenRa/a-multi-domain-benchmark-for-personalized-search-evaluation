import json
import logging
import os

import click
import torch
import tqdm
from ranx import Qrels, Run, compare, evaluate

from dataloader.utils import load_test_query

logger = logging.getLogger(__name__)

@click.command()
@click.option(
    "--embedding_folder",
    type=str,
    required=True,
)
@click.option(
    "--domain_path",
    type=str,
    required=True,
)
@click.option(
    "--split",
    type=click.Choice(
        [
            "train",
            "val",
            "test",
        ]
    ),
    required=True,
    help="Split if data to evaluate.",
)
@click.option(
    "--mu",
    type=float,
    required=False,
    default=0.5
)
def main(
    embedding_folder,
    domain_path,
    split,
    mu
):
    logging_file = f"personalized_testing_{domain_path.split('/')[-1]}.log"
    logging.basicConfig(filename=os.path.join('../logs', logging_file),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO
                        )
    logger.debug('Loading Embedding File and id_to_index dictionary.')
    doc_embedding = torch.load(os.path.join(embedding_folder, 'collection_embedding.pt'))
    with open(os.path.join(embedding_folder, 'id_to_index.json'), 'r') as f:
        id_to_index = json.load(f)

    logger.debug('Loading models and tokenizer.')

    queries_file = f'{split}/queries.jsonl'
    filename = os.path.join(domain_path, queries_file)
    data = load_test_query(filename)

    test_qrels = {}
    bert_run = {}
    bm25_run = {}
    for d in tqdm.tqdm(data, total=len(data)):
        user_docs = data[d]['user_docs']
        q_embedding = doc_embedding[torch.tensor([int(id_to_index[x]) for x in user_docs])].mean(0, keepdim=True)
        d_qrels = {k: 1 for k in data[d]['relevant_docs']}
        test_qrels[d] = d_qrels
        
        bm25_docs = data[d]['bm25_docs']
        d_embeddings = doc_embedding[torch.tensor([int(id_to_index[x]) for x in bm25_docs])]
        
        bert_scores = torch.einsum('xy, ly -> x', d_embeddings, q_embedding)
        
        bm25_run[d] = {doc_id: data[d]['bm25_scores'][i] for i, doc_id in enumerate(bm25_docs)}
        bert_run[d] = {doc_id: bert_scores[i].item() for i, doc_id in enumerate(bm25_docs)}
    
    qrels = Qrels(test_qrels)

    best_score = 0
    if split == 'val':
        mus = [i/10 for i in range(0,11)]
        weight_bert_bm25 = {}
        for m in mus:
            weight_bert_bm25 = {}
            for d in bert_run:
                max_bm25_res = max([bm25_run[d][doc] for doc in bm25_run[d]])
                weight_bert_bm25[d] = {doc: (m * bm25_run[d][doc]/max_bm25_res) + ((1 - m) * bert_run[d][doc]) for doc in bm25_run[d]}
            ranx_bert_bm25_run = Run(weight_bert_bm25)
            score = evaluate(
                qrels=qrels,
                run=ranx_bert_bm25_run,
                metrics='map@100'
            )
            if score > best_score:
                best_score = score
                mu = m
            logging.info(f'Mu: {m}, Score: {round(score ,5)}')
            print(f'Mu: {m}, Score: {round(score ,5)}')
            
    logging.info(f'Reporting {domain_path} results with mu: {mu}')
    weight_bert_bm25 = {}
    for d in bert_run:
        max_bm25_res = max([bm25_run[d][doc] for doc in bm25_run[d]])
        weight_bert_bm25[d] = {doc: (mu * bm25_run[d][doc]/max_bm25_res) + ((1 - mu) * bert_run[d][doc]) for doc in bm25_run[d]}

    logger.debug('Saving bm25_run file')
    with open(os.path.join(domain_path, 'bm25_run.json'), 'w') as f:
        json.dump(bm25_run, f)
    logger.debug('Saving berts file')
    with open(os.path.join(domain_path, 'bert_run.json'), 'w') as f:
        json.dump(bert_run, f)

    logger.debug('Evaluating with Ranx')
    ranx_bm25_run = Run(bm25_run)
    ranx_bert_run = Run(bert_run)
    ranx_bert_bm25_run = Run(weight_bert_bm25)

    report = compare(
        qrels=qrels,
        runs=[ranx_bert_run, ranx_bm25_run, ranx_bert_bm25_run],
        metrics=['map@100', 'mrr@100', 'ndcg@100', 'mrr@10', 'ndcg@10'],
        max_p=0.01  # P-value threshold
    )
    logger.info(f'\n{report}')
    print(report)

if __name__ == '__main__':
    main()
