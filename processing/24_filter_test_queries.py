import json

import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl
from src.to_timestamp import year_to_timestamp


def load_test_queries(dataset_path: str):
    split_path = join_path(dataset_path, "test")
    queries_path = join_path(split_path, "queries.jsonl")
    return read_jsonl(queries_path)


def save_test_queries(dataset_path: str, queries: list):
    split_path = join_path(dataset_path, "test")
    queries_path = join_path(split_path, "queries.jsonl")
    write_jsonl(queries, queries_path)


def load_paper_dates(dataset_path):
    papers_path = join_path(dataset_path, "papers.jsonl")

    paper_date_dict = {}
    with open(papers_path, "r") as papers_f:
        for line in papers_f:
            paper = json.loads(line)
            paper_id = paper["id"]
            paper_date_dict[paper_id] = paper["timestamp"]

    return paper_date_dict


def filter_relevants(paper_date_dict, queries, timestamp, min_rel):
    for q in queries:
        q["rel_doc_ids"] = [
            doc_id
            for doc_id in q["rel_doc_ids"]
            if paper_date_dict[doc_id] < timestamp
        ]

    return [q for q in queries if len(q["rel_doc_ids"]) >= min_rel]


def filter_user_docs(paper_date_dict, queries, timestamp, min_user_docs):
    for q in queries:
        q["user_doc_ids"] = [
            doc_id
            for doc_id in q["user_doc_ids"]
            if paper_date_dict[doc_id] < timestamp
        ]

    return [q for q in queries if len(q["user_doc_ids"]) >= min_user_docs]


@click.command()
@click.option("--fos", required=True)
@click.option("--lang", default="en")
@click.option("--min_rel", default=1)
@click.option("--min_user_docs", default=20)
@click.option("--year", default=2019)
def main(lang, fos, min_rel, min_user_docs, year):
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)

    print(f"{fos} : Filtering test queries")
    dataset_path = join_path(lang_path, fos)

    timestamp = year_to_timestamp(year)
    paper_date_dict = load_paper_dates(dataset_path)

    queries = load_test_queries(dataset_path)

    queries = filter_relevants(paper_date_dict, queries, timestamp, min_rel)
    queries = filter_user_docs(
        paper_date_dict, queries, timestamp, min_user_docs
    )

    save_test_queries(dataset_path, queries)


if __name__ == "__main__":
    main()
