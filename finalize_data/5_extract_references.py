from collections import defaultdict

import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl


def load_collection(dataset_path: str):
    collection_path = join_path(dataset_path, "collection.jsonl")
    docs = read_jsonl(collection_path)
    return [{"id": x["id"], "timestamp": x["timestamp"]} for x in docs]


def load_references(dataset_path: str):
    references_path = join_path(dataset_path, "paper_references.jsonl")
    return read_jsonl(references_path)


def get_in_and_out_refs(docs: list, references: list[dict]):
    doc_ids = {x["id"] for x in docs}
    doc_date_dict = {
        x["id"]: {"doc_id": x["id"], "timestamp": x["timestamp"]} for x in docs
    }
    in_references = defaultdict(list)
    out_references = defaultdict(list)

    for x in references:
        doc_id = x["doc_id"]
        rel_doc_ids = x["rel_doc_ids"]

        if doc_id not in doc_ids:
            continue

        # Sanity check
        assert all(id for id in rel_doc_ids if id in doc_ids)

        doc = doc_date_dict[doc_id]
        for rel_doc_id in rel_doc_ids:
            in_references[rel_doc_id].append(doc)

        out_references[doc_id] = {
            "timestamp": doc["timestamp"],
            "doc_ids": rel_doc_ids,
        }

    in_references = [
        {"doc_id": k, "in_refs": v} for k, v in in_references.items()
    ]

    out_references = [
        {"doc_id": k, "timestamp": v["timestamp"], "out_refs": v["doc_ids"]}
        for k, v in out_references.items()
    ]

    return in_references, out_references


@click.command()
@click.option("--fos", required=True)
@click.option("--lang", required=True, default="en")
def main(lang, fos):
    dataset_path = join_path("tmp", "datasets", lang, fos)
    final_dataset_path = join_path("datasets", lang, fos)
    in_refs_path = join_path(final_dataset_path, "in_refs.jsonl")
    out_refs_path = join_path(final_dataset_path, "out_refs.jsonl")

    print("Loading collection")
    docs = load_collection(final_dataset_path)

    print("Loading references")
    references = load_references(dataset_path)

    print("Getting in and out references")
    in_references, out_references = get_in_and_out_refs(docs, references)

    print("Saving references")
    write_jsonl(in_references, in_refs_path)
    write_jsonl(out_references, out_refs_path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
