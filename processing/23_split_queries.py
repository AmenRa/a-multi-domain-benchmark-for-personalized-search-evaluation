import os

import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl
from src.to_timestamp import year_to_timestamp


def split_train_test(queries: list, year: int):
    timestamp = year_to_timestamp(year)
    train_set = [x for x in queries if x["timestamp"] < timestamp]
    test_set = [x for x in queries if x["timestamp"] >= timestamp]
    return train_set, test_set


def save_split(dataset_path: str, split: str, queries: list):
    split_path = join_path(dataset_path, split)
    queries_path = join_path(split_path, "queries.jsonl")
    os.makedirs(split_path, exist_ok=True)
    write_jsonl(queries, queries_path)


def load_queries(dataset_path: str):
    queries_path = join_path(dataset_path, "queries.jsonl")
    return read_jsonl(queries_path)


@click.command()
@click.argument("fos_list", nargs=-1)
@click.option("--lang", default="en")
@click.option("--year", default=2019)
def main(lang, fos_list, year):
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)
    for i, fos in enumerate(fos_list):
        print(f"{i+1}/{len(fos_list)} {fos}")
        dataset_path = join_path(lang_path, fos)

        print("Loading queries")
        queries = load_queries(dataset_path)

        print("Splitting queries")
        train_set, test_set = split_train_test(queries, year)
        print(f"train: {len(train_set)}")
        print(f"test: {len(test_set)}")

        print("Saving queries")
        save_split(dataset_path, "train", train_set)
        save_split(dataset_path, "test", test_set)


if __name__ == "__main__":
    # execute only if run as a script
    main()
