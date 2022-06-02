from collections import defaultdict

import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl


def load_authors(dataset_path: str):
    authors_path = join_path(dataset_path, "authors.jsonl")
    return read_jsonl(authors_path)


def load_doc_ids(dataset_path: str):
    collection_path = join_path(dataset_path, "collection.jsonl")
    return {d["id"] for d in read_jsonl(collection_path)}


def filter_authors(authors, paper_authors):
    doc_ids = {d["doc_id"] for d in paper_authors}
    author_ids = {
        author_id for d in paper_authors for author_id in d["author_ids"]
    }

    authors = [x for x in authors if x["id"] in author_ids]

    for a in authors:
        a["docs"] = [d for d in a["docs"] if d["doc_id"] in doc_ids]

    return authors


def get_relations(authors: list[dict]):
    has_authors = defaultdict(list)

    for x in authors:
        author_id = x["id"]
        docs = x["docs"]

        for doc in docs:
            if doc["doc_id"] not in has_authors:
                has_authors[doc["doc_id"]] = {
                    "timestamp": doc["timestamp"],
                    "author_ids": [author_id],
                }
            else:
                has_authors[doc["doc_id"]]["author_ids"].append(author_id)

    has_authors = [
        {
            "doc_id": k,
            "timestamp": v["timestamp"],
            "author_ids": v["author_ids"],
        }
        for k, v in has_authors.items()
    ]

    return has_authors


@click.command()
@click.option("--fos", required=True)
@click.option("--lang", required=True, default="en")
def main(lang, fos):
    dataset_path = join_path("tmp", "datasets", lang, fos)
    final_dataset_path = join_path("datasets", lang, fos)

    paper_authors_path = join_path(dataset_path, "paper_authors.jsonl")
    authors_path = join_path(final_dataset_path, "authors.jsonl")
    has_authors_path = join_path(final_dataset_path, "has_authors.jsonl")

    print("Loading collection")
    doc_ids = load_doc_ids(final_dataset_path)

    print("Loading paper authors")
    paper_authors = read_jsonl(paper_authors_path)
    paper_authors = [x for x in paper_authors if x["doc_id"] in doc_ids]

    print("Loading authors")
    authors = load_authors(dataset_path)

    print("Filtering authors")
    authors = filter_authors(authors, paper_authors)

    print("Getting authorship relations")
    has_authors = get_relations(authors)

    print("Saving data")
    write_jsonl(authors, authors_path)
    write_jsonl(has_authors, has_authors_path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
