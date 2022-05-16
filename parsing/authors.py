import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def new_author():
    return {
        "id": "",
        "name": "",
        "affiliation_id": "",
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "02.Authors.nt.bz2")
    write_path = join_path(raw_data_path, "authors.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        author = new_author()

        for line in tqdm(
            f_in,
            desc="Parsing authors",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            parts = line[1:-4].split("> <")

            if len(parts) == 3:
                subject, predicate, object = parts
            else:
                subject, predicate = parts

            id = subject.split("/")[-1]

            if author["id"] != id:
                if author["id"] != "":
                    f_out.write(json.dumps(author) + "\n")
                    author = new_author()
                author["id"] = id

            if "memberOf" in predicate:
                author["affiliation_id"] = object.split("/")[-1]

            if "name" in predicate:
                author["name"] = normalize_str(predicate.split('"')[1])

        f_out.write(json.dumps(author) + "\n")


if __name__ == "__main__":
    main()
