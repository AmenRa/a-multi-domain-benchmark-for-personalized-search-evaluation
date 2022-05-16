import json
import sys
from collections import deque

from elasticsearch import helpers
from tqdm import tqdm

from .oneliner_utils import chunk_by_size, count_lines


def doc_generator(collection_path, index_name):
    n_lines = count_lines(collection_path)

    with open(collection_path, "r") as f:
        for _ in tqdm(range(n_lines), desc="Indexing documents"):
            line = f.readline()

            if not line or line == "":
                break

            doc = json.loads(line)

            yield {
                "_index": index_name,
                "_source": doc,
            }


def index_jsonl(
    es_client,
    index_name,
    collection_path,
    index_config=None,
    threads=8,
):
    if index_config is None:
        index_config = {
            "mappings": {
                "properties": {
                    "id": {"type": "text"},
                    "contents": {
                        "type": "text",
                        "analyzer": "whitespace",
                        "similarity": "ranking_function",
                    },
                    "timestamp": {"type": "integer"},
                }
            },
            "settings": {
                "number_of_shards": 1,
                "index": {
                    "similarity": {
                        "ranking_function": {
                            "type": "BM25",
                            "b": 0.75,
                            "k1": 1.2,
                        }
                    }
                },
            },
        }

    es_client.indices.delete(index=index_name, ignore=[400, 404])
    es_client.indices.create(index=index_name, body=index_config)

    try:
        deque(
            helpers.parallel_bulk(
                es_client,
                doc_generator(collection_path, index_name),
                thread_count=threads,
                chunk_size=500,
                raise_on_error=True,
                request_timeout=10000,
            ),
            maxlen=0,
        )
    except RuntimeError as e:
        print(e)


def search(es_client, index_name, query, timestamp, size):
    res = es_client.search(
        index=index_name,
        body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "contents": {
                                    "query": query,
                                    "operator": "or",
                                }
                            }
                        },
                    ],
                    "filter": [
                        {"range": {"timestamp": {"lt": timestamp}}},
                    ],
                }
            }
        },
        size=size,
    )

    return res["hits"]["hits"]


def msearch(
    es_client,
    index_name,
    queries,
    size=100,
    show_progress=True,
    pbar_desc="Running queries",
):
    chunk_size = 100
    chunks = chunk_by_size(queries, chunk_size)
    results = []

    # Create progress bar
    pbar = tqdm(
        total=len(queries),
        desc=pbar_desc,
        disable=not show_progress,
        dynamic_ncols=True,
    )

    for chunk in chunks:
        es_queries = []

        for q in chunk:
            query = q["text"]
            timestamp = q["timestamp"]

            assert timestamp >= 0, "Timestamp error"

            # req_head
            es_queries.append({"index": index_name})
            # req_body
            es_queries.append(
                {
                    "_source": ["id"],
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match": {
                                        "contents": {
                                            "query": query,
                                            "operator": "or",
                                        }
                                    }
                                },
                            ],
                            "filter": [
                                {"range": {"timestamp": {"lt": timestamp}}},
                            ],
                        }
                    },
                    "size": size,
                }
            )

        request = ""
        for q in es_queries:
            request += "%s \n" % json.dumps(q)

        res = es_client.msearch(body=request)
        results += [x["hits"]["hits"] for x in res["responses"]]

        pbar.update(len(chunk))
    pbar.close()

    results = [
        [(x["_source"]["id"], x["_score"]) for x in res] for res in results
    ]

    return results


def set_bm25(es_client, index_name, b=0.75, k1=1.2):
    es_client.indices.close(
        index=index_name, wait_for_active_shards="index-setting"
    )

    es_client.indices.put_settings(
        index=index_name,
        body={
            "index": {
                "similarity": {
                    "ranking_function": {"type": "BM25", "b": b, "k1": k1}
                }
            }
        },
    )

    es_client.indices.open(index=index_name)
