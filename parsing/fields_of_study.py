import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def new_fos():
    return {
        "id": "",
        "name": "",
        "level": "",
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "15.FieldsOfStudy.nt.bz2")
    write_path = join_path(raw_data_path, "fields_of_study.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        fos = new_fos()

        for line in tqdm(
            f_in,
            desc="Parsing papers",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            subject, predicate = line[1:-4].split("> <")[:2]
            id = subject.split("/")[-1]

            if fos["id"] != id:
                if fos["id"] != "":
                    f_out.write(json.dumps(fos) + "\n")
                    fos = new_fos()
                fos["id"] = id

            if "name" in predicate:
                fos["name"] = normalize_str(predicate.split('"')[1])
            elif "level" in predicate:
                fos["level"] = int(predicate.split('"')[1])

        f_out.write(json.dumps(fos) + "\n")


if __name__ == "__main__":
    main()
