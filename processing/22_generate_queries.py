import json

import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl
from src.preprocessing import preprocessing
from tqdm import tqdm

"""
query = {
    id:
    text:
    user_id:
    rel_doc_ids:
    user_doc_ids:
    timestamp:
}
"""


def filter_queries_by_min_user_docs(queries, min_user_docs=5):
    return [
        x
        for x in tqdm(
            queries,
            desc=f"Removing queries with less than {min_user_docs} associated user docs",
            mininterval=1.0,
            dynamic_ncols=True,
        )
        if len(x["user_doc_ids"]) >= min_user_docs
    ]


def filter_queries_by_min_relevants(queries, min_rel=1):
    return [
        x
        for x in tqdm(
            queries,
            desc=f"Removing queries with less than {min_rel} relevants",
            mininterval=1.0,
            dynamic_ncols=True,
        )
        if len(x["rel_doc_ids"]) >= min_rel
    ]


def filter_queries_with_no_user(queries):
    return [
        x
        for x in tqdm(
            queries,
            desc="Removing queries with no user",
            mininterval=1.0,
            dynamic_ncols=True,
        )
        if x["user_id"]
    ]


def add_user_docs(dataset_path, queries):
    authors_path = join_path(dataset_path, "authors.jsonl")
    authors_dict = {x["id"]: x["docs"] for x in read_jsonl(authors_path)}

    queries = [
        q
        | {
            "user_doc_ids": [
                x["doc_id"]
                for x in authors_dict[q["user_id"]]
                if x["timestamp"] < q["timestamp"]
            ]
        }
        for q in tqdm(
            queries,
            desc="Adding users' documents",
            mininterval=1.0,
            dynamic_ncols=True,
        )
    ]

    # Sanity check
    for q in queries:
        assert (
            q["id"] not in q["user_doc_ids"]
        ), "Error: query_id in user_doc_ids"

    return queries


def add_user(dataset_path, queries):
    paper_authors_path = join_path(dataset_path, "paper_authors.jsonl")
    paper_author_dict = {
        x["doc_id"]: x["author_ids"][0] for x in read_jsonl(paper_authors_path)
    }

    return [
        x | {"user_id": paper_author_dict.get(x["id"], False)}
        for x in tqdm(
            queries, desc="Adding users", mininterval=1.0, dynamic_ncols=True
        )
    ]


def add_relevants(dataset_path, queries):
    paper_references_path = join_path(dataset_path, "paper_references.jsonl")
    paper_references_dict = {
        x["doc_id"]: x["rel_doc_ids"] for x in read_jsonl(paper_references_path)
    }

    return [
        x | {"rel_doc_ids": paper_references_dict.get(x["id"], [])}
        for x in tqdm(
            queries,
            desc="Adding relevants",
            mininterval=1.0,
            dynamic_ncols=True,
        )
    ]


def generate_title_queries(dataset_path: str):
    papers_path = join_path(dataset_path, "papers.jsonl")

    queries = []

    with open(papers_path, "r") as papers_f:
        for line in tqdm(
            papers_f,
            desc="Generating queries",
            mininterval=1.0,
            dynamic_ncols=True,
        ):
            paper = json.loads(line)

            query = {
                "id": paper["id"],
                "text": preprocessing(paper["title"]),
                "timestamp": paper["timestamp"],
            }

            queries.append(query)

    return queries


@click.command()
@click.argument("fos_list", nargs=-1)
@click.option("--lang", default="en")
@click.option("--min_rel", default=1)
@click.option("--min_user_docs", default=20)
def main(lang, fos_list, min_rel, min_user_docs):
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)

    for i, fos in enumerate(fos_list):
        print(f"{i+1}/{len(fos_list)} - {fos}")
        dataset_path = join_path(lang_path, fos)

        queries = generate_title_queries(dataset_path)
        queries = add_relevants(dataset_path, queries)
        queries = filter_queries_by_min_relevants(queries, min_rel)
        queries = add_user(dataset_path, queries)
        queries = filter_queries_with_no_user(queries)
        queries = add_user_docs(dataset_path, queries)
        queries = filter_queries_by_min_user_docs(queries, min_user_docs)

        print("n queries :", len(queries), "\n")
        write_jsonl(queries, join_path(dataset_path, "queries.jsonl"))


if __name__ == "__main__":
    main()
