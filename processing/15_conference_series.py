import json
from multiprocessing import Pool

import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl
from tqdm import tqdm


def get_conference_series(lang: str, fos: str, prog_bar_position: int):
    # Folder paths
    raw_data_path = join_path("tmp", "raw_data")
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)
    dataset_path = join_path(lang_path, fos)

    # File paths
    papers_path = join_path(dataset_path, "papers.jsonl")
    conference_series_path = join_path(raw_data_path, "conference_series.jsonl")
    write_path = join_path(dataset_path, "conference_series.jsonl")

    conference_serie_ids = set()

    with open(papers_path, "r") as papers_f:
        for line in tqdm(
            papers_f,
            mininterval=1.0,
            desc=fos,
            dynamic_ncols=True,
            position=prog_bar_position,
        ):
            paper = json.loads(line)
            if paper["conference_series_id"]:
                conference_serie_ids.add(paper["conference_series_id"])

    conference_series = read_jsonl(conference_series_path)
    conference_series = [
        x for x in conference_series if x["id"] in conference_serie_ids
    ]

    write_jsonl(conference_series, write_path)


@click.command()
@click.argument("fos_list", nargs=-1)
@click.option("--lang", default="en")
def main(lang, fos_list):
    with Pool(len(fos_list)) as pool:
        pool.starmap(
            get_conference_series,
            [(lang, fos, i) for i, fos in enumerate(fos_list)],
        )


if __name__ == "__main__":
    main()
