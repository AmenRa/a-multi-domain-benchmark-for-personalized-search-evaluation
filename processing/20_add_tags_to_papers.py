import json
import os

import click
from src.oneliner_utils import join_path, read_jsonl
from tqdm import tqdm


def add_tags(lang: str, fos: str):
    # Folder paths
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)
    dataset_path = join_path(lang_path, fos)
    final_dataset_path = join_path("datasets", lang, fos)
    os.makedirs(final_dataset_path, exist_ok=True)

    # File paths
    tags_path = join_path(dataset_path, "paper_tags.jsonl")
    collection_path = join_path(final_dataset_path, "collection.jsonl")

    papers_dict = {x["id"]: x for x in read_jsonl(collection_path)}

    with open(tags_path, "r") as tags_f, open(collection_path, "w") as write_f:
        for line in tqdm(
            tags_f,
            mininterval=1.0,
            desc="Adding tags",
            dynamic_ncols=True,
        ):
            tag = json.loads(line)
            doc_id = tag["doc_id"]
            paper = papers_dict.get(doc_id, False)
            if paper:
                paper["keywords"] = tag["keywords"]
                write_f.write(json.dumps(paper) + "\n")
                del papers_dict[doc_id]
            # else:
            #     print(doc_id, "not found")


@click.command()
@click.argument("fos_list", nargs=-1)
@click.option("--lang", default="en")
def main(lang, fos_list):
    for i, fos in enumerate(fos_list):
        print(f"{i+1}/{len(fos_list)} - {fos}")
        add_tags(lang, fos)


if __name__ == "__main__":
    main()
