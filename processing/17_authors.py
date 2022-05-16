import json
from collections import defaultdict

import click
from src.oneliner_utils import join_path, read_jsonl
from tqdm import tqdm

fos_list = [
    # "history",
    # "biology",
    # "medicine",
    "computer_science",
    # "environmental_science",
    # "mathematics",
    # "geography",
    # "materials_science",
    # "chemistry",
    # "political_science",
    # "economics",
    # "psychology",
    # "business",
    # "sociology",
    # "art",
    # "philosophy",
    # "engineering",
    # "geology",
    # "physics",
]


def get_authors(lang: str, fos: str):
    # Folder paths
    raw_data_path = join_path("tmp", "raw_data")
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)
    dataset_path = join_path(lang_path, fos)

    # File paths
    authors_path = join_path(raw_data_path, "authors.jsonl")
    paper_authors_path = join_path(dataset_path, "paper_authors.jsonl")
    papers_path = join_path(dataset_path, "papers.jsonl")
    write_path = join_path(dataset_path, "authors.jsonl")

    # --------------------------------------------------------------------------
    paper_authors_dict = {
        x["doc_id"]: x for x in read_jsonl(paper_authors_path)
    }

    with open(papers_path, "r") as papers_f:
        for line in papers_f:
            paper = json.loads(line)
            paper_authors_dict[paper["id"]]["timestamp"] = paper["timestamp"]

    author_papers_dict = defaultdict(list)
    for x in paper_authors_dict.values():
        for author_id in x["author_ids"]:
            author_papers_dict[author_id].append(
                {"doc_id": x["doc_id"], "timestamp": x["timestamp"]}
            )

    del paper_authors_dict
    author_ids = set(author_papers_dict)

    # Filter authors -----------------------------------------------------------
    with open(authors_path, "r") as authors_f, open(write_path, "w") as f_out:
        for line in tqdm(
            authors_f,
            mininterval=1.0,
            desc=fos,
            dynamic_ncols=True,
        ):
            author = json.loads(line)

            if author["id"] in author_ids:
                author["docs"] = author_papers_dict[author["id"]]
                f_out.write(json.dumps(author) + "\n")


@click.command()
@click.option("--lang", default="en")
def main(lang):
    for fos in fos_list:
        get_authors(lang, fos)


if __name__ == "__main__":
    main()
