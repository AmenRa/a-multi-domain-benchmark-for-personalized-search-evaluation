import json
from multiprocessing import Pool

import click
from src.oneliner_utils import join_path, read_list
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


def get_paper_tags(lang: str, fos: str, prog_bar_position: int):
    # Folder paths
    raw_data_path = join_path("tmp", "raw_data")
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)
    dataset_path = join_path(lang_path, fos)

    # File paths
    doc_ids_path = join_path(dataset_path, "doc_ids.txt")
    tags_path = join_path(raw_data_path, "paper_tags.jsonl")
    write_path = join_path(dataset_path, "paper_tags.jsonl")

    doc_ids = set(read_list(doc_ids_path))

    with open(tags_path, "r") as tags_f, open(write_path, "w") as f_out:
        for line in tqdm(
            tags_f,
            mininterval=1.0,
            desc=fos,
            dynamic_ncols=True,
            position=prog_bar_position,
        ):
            tag = json.loads(line)
            if tag["doc_id"] in doc_ids:
                f_out.write(line.strip() + "\n")


@click.command()
@click.option("--lang", default="en")
def main(lang):
    with Pool(len(fos_list)) as pool:
        pool.starmap(
            get_paper_tags,
            [(lang, fos, i) for i, fos in enumerate(fos_list)],
        )


if __name__ == "__main__":
    main()
