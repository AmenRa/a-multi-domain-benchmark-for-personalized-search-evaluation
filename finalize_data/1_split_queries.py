import math
import os
import random

import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl


def split_train_val(train_set, train_ratio=0.99):
    random.shuffle(train_set)
    val_set = train_set[math.ceil(len(train_set) * train_ratio) :]
    train_set = train_set[: math.ceil(len(train_set) * train_ratio)]
    return train_set, val_set


# def split_train_val(train_set, n_val_queries=5_000):
#     random.shuffle(train_set)
#     val_set = train_set[:n_val_queries]
#     train_set = train_set[n_val_queries:]
#     return train_set, val_set


def filter_by_min_rels(queries, min_rels=10):
    return [x for x in queries if len(x["rel_doc_ids"]) >= min_rels]


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
    "--seed",
    required=True,
    default=42,
    help="Random seed to be used. Defaults to 42.",
)
def main(lang, fos, seed):
    random.seed(seed)

    # Folder paths
    dataset_path = join_path("tmp", "datasets", lang, fos)
    final_dataset_path = join_path("datasets", lang, fos)
    train_set_path = join_path(final_dataset_path, "train")
    val_set_path = join_path(final_dataset_path, "val")
    test_set_path = join_path(final_dataset_path, "test")
    os.makedirs(train_set_path, exist_ok=True)
    os.makedirs(val_set_path, exist_ok=True)
    os.makedirs(test_set_path, exist_ok=True)

    # File paths
    train_set_read_path = join_path(dataset_path, "train", "bm25_queries.jsonl")
    test_set_read_path = join_path(dataset_path, "test", "bm25_queries.jsonl")
    #
    train_set_write_path = join_path(train_set_path, "queries.jsonl")
    val_set_write_path = join_path(val_set_path, "queries.jsonl")
    test_set_write_path = join_path(test_set_path, "queries.jsonl")

    # Load queries -------------------------------------------------------------
    train_set = read_jsonl(train_set_read_path)
    test_set = read_jsonl(test_set_read_path)

    # Split queries ------------------------------------------------------------
    train_set, val_set = split_train_val(train_set)

    # Filter queries -----------------------------------------------------------
    test_set = filter_by_min_rels(test_set, 10)

    # Save queries -------------------------------------------------------------
    write_jsonl(train_set, train_set_write_path)
    write_jsonl(val_set, val_set_write_path)
    write_jsonl(test_set, test_set_write_path)

    print(f"train: {len(train_set)}")
    print(f"val: {len(val_set)}")
    print(f"test: {len(test_set)}")


if __name__ == "__main__":
    # execute only if run as a script
    main()
