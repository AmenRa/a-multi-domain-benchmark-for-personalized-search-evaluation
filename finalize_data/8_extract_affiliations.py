import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl


def load_authors(dataset_path: str):
    authors_path = join_path(dataset_path, "authors.jsonl")
    return read_jsonl(authors_path)


def load_affiliations(raw_data_path: str):
    affiliations_path = join_path(raw_data_path, "affiliations.jsonl")
    return {
        x["id"]: x | {"user_ids": []} for x in read_jsonl(affiliations_path)
    }


def filter_authors(authors, docs):
    author_ids = {author_id for d in docs for author_id in d["author_ids"]}
    return [x for x in authors if x["id"] in author_ids]


def enrich_affiliations(affiliations: dict, authors: list[dict]):
    for x in authors:
        author_id = x["id"]
        affiliation_id = x["affiliation_id"]

        if len(affiliation_id) > 0:
            affiliations[affiliation_id]["user_ids"].append(author_id)

    affiliations = [v for v in affiliations.values() if len(v["user_ids"]) > 0]

    return affiliations


@click.command()
@click.option("--fos", required=True)
@click.option("--lang", required=True, default="en")
def main(lang, fos):
    raw_data_path = join_path("tmp", "raw_data")
    dataset_path = join_path("datasets", lang, fos)

    affiliations_path = join_path(dataset_path, "affiliations.jsonl")

    print("Loading authors")
    authors = load_authors(dataset_path)

    print("Loading affiliations")
    affiliations = load_affiliations(raw_data_path)

    print("Getting affiliated authors")
    affiliations = enrich_affiliations(affiliations, authors)

    print("Saving data")
    write_jsonl(affiliations, affiliations_path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
