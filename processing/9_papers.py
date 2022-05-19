import json
from multiprocessing import Pool

import click
from src.oneliner_utils import join_path, read_list
from tqdm import tqdm


def get_papers_by_fos(lang: str, fos: str, prog_bar_position: int):
    # Folder paths
    raw_data_path = join_path("tmp", "raw_data")
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)
    dataset_path = join_path(lang_path, fos)

    # File paths
    doc_ids_path = join_path(dataset_path, "final_doc_ids.txt")
    papers_path = join_path(raw_data_path, "papers.jsonl")
    write_path = join_path(dataset_path, "papers.jsonl")

    doc_ids = set(read_list(doc_ids_path))

    with open(papers_path, "r") as papers_f, open(write_path, "w") as f_out:
        for line in tqdm(
            papers_f,
            mininterval=1.0,
            desc=fos,
            dynamic_ncols=True,
            position=prog_bar_position,
        ):
            paper = json.loads(line)
            if paper["id"] in doc_ids:
                f_out.write(line.strip() + "\n")


@click.command()
@click.argument("fos_list", nargs=-1)
@click.option("--lang", default="en")
def main(lang, fos_list):
    with Pool(len(fos_list)) as pool:
        pool.starmap(
            get_papers_by_fos,
            [(lang, fos, i) for i, fos in enumerate(fos_list)],
        )


if __name__ == "__main__":
    main()
