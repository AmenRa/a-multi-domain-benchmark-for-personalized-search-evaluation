import bz2
import json
import os
from unittest import main

from src.oneliner_utils import join_path
from tqdm import tqdm


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "16.PaperFieldsOfStudy.nt.bz2")
    write_path = join_path(raw_data_path, "paper_fields_of_study.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        for line in tqdm(
            f_in,
            desc="Parsing papers",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            doc_id, _, fos_id = line[1:-4].split("> <")
            paper_fos = {
                "doc_id": doc_id.split("/")[-1],
                "fos_id": fos_id.split("/")[-1],
            }
            f_out.write(json.dumps(paper_fos) + "\n")


if __name__ == "__main__":
    main()
