import os

import click
from elasticsearch import Elasticsearch
from src.elasticsearch_utils import index_jsonl
from src.oneliner_utils import join_path


@click.command()
@click.option(
    "--lang",
    required=True,
    default="en",
)
@click.option(
    "--fos",
    required=True,
)
@click.option(
    "--threads",
    default=4,
    help="Number of threads to use to index the collection. Defaults to 4.",
)
def main(lang, fos, threads):
    # Create connection with Elasticsearch
    es_client = Elasticsearch(timeout=180)

    # Index collection from JSONl
    index_jsonl(
        es_client=es_client,
        index_name="academic-search",
        collection_path=join_path(
            "tmp", "datasets", lang, fos, "bm25_collection.jsonl"
        ),
        threads=threads,
    )


if __name__ == "__main__":
    # execute only if run as a script
    main()
