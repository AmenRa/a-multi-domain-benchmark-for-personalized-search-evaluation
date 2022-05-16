import bz2
import json
import os
from unittest import main

from src.oneliner_utils import join_path
from tqdm import tqdm


def new_fos():
    return {
        "id": "",
        "parent_id": "",
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "13.FieldOfStudyChildren.nt.bz2")
    write_path = join_path(raw_data_path, "field_of_study_children.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        fos = new_fos()

        for line in tqdm(
            f_in,
            desc="Parsing foss",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            parts = line[1:-4].split("> <")
            subject, _, object = parts
            id = subject.split("/")[-1]

            if fos["id"] != id:
                if fos["id"] != "":
                    f_out.write(json.dumps(fos) + "\n")
                    fos = new_fos()
                fos["id"] = id

            fos["parent"] = object.split("/")[-1]

        f_out.write(json.dumps(fos) + "\n")


if __name__ == "__main__":
    main()
