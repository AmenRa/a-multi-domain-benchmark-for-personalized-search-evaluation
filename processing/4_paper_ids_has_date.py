import json
import os

import click
from src.oneliner_utils import join_path, read_list, write_list
from tqdm import tqdm

fos_list = [
    "history",
    "biology",
    "medicine",
    "computer_science",
    "environmental_science",
    "mathematics",
    "geography",
    "materials_science",
    "chemistry",
    "political_science",
    "economics",
    "psychology",
    "business",
    "sociology",
    "art",
    "philosophy",
    "engineering",
    "geology",
    "physics",
]


@click.command()
@click.option("--lang", default="en")
def main(lang):
    # Folder paths
    raw_data_path = join_path("tmp", "raw_data")
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)

    doc_ids_by_fos_dict = {}
    for fos in fos_list:
        dataset_path = join_path(lang_path, fos)
        doc_ids_path = join_path(dataset_path, "doc_ids.txt")
        doc_ids = set(read_list(doc_ids_path))
        doc_ids_by_fos_dict[fos] = doc_ids

    papers_path = join_path(raw_data_path, "papers.jsonl")

    date_ids = set()
    with open(papers_path, "r") as f_in:
        for line in tqdm(
            f_in,
            mininterval=1.0,
            desc="Filtering doc ids with no date",
            dynamic_ncols=True,
        ):
            paper = json.loads(line)
            if len(paper["publication_date"]) > 0:
                date_ids.add(paper["id"])

    for fos, doc_ids in doc_ids_by_fos_dict.items():
        dataset_path = join_path(lang_path, fos)
        os.makedirs(dataset_path, exist_ok=True)
        write_path = join_path(dataset_path, "doc_ids.txt")
        print(f"{fos} {len(doc_ids)}")
        write_list(list(set.intersection(doc_ids, date_ids)), write_path)


if __name__ == "__main__":
    main()
