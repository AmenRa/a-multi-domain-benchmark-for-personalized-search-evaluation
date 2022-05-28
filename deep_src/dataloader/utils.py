import json
import logging
import os
import random

import numpy as np
import torch
import tqdm

logger = logging.getLogger(__name__)


def seed_everything(seed: int):
    logger.info(f'Setting global random seed to {seed}')
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def load_jsonl(file: str):
    with open(file, 'r') as f:
        for lne in f:
            yield json.loads(lne)

def load_query_data(file: str, verbose: bool=True):
    with open(file, 'r') as f:
        query_file = {}
        pbar = tqdm.tqdm(f, desc='Creating data for loading') if verbose else f
        for lne in pbar:
            query_json = json.loads(lne)
            bm_25_not_relevant_docs = [id_ for id_ in query_json['bm25_doc_ids'] if id_ not in query_json['rel_doc_ids']]
            if bm_25_not_relevant_docs:
                query_file[query_json['id']] = {
                    'text': query_json['text'],
                    'relevant_docs': query_json['rel_doc_ids'],
                    'bm25_docs': bm_25_not_relevant_docs
                }

        return query_file


def load_test_query(file):
    with open(file, 'r') as f:
        query_file = {}
        for lne in tqdm.tqdm(f):
            query_json = json.loads(lne)
            query_file[query_json['id']] = {
                'text': query_json['text'],
                'relevant_docs': query_json['rel_doc_ids'],
                'bm25_docs': query_json['bm25_doc_ids'],
                'bm25_scores': query_json['bm25_doc_scores'],
                'user_docs': query_json['user_doc_ids']
            }
            
        return query_file
    