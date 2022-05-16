import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def new_affiliation():
    return {
        "id": "",
        "name": "",
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "01.Affiliations.nt.bz2")
    write_path = join_path(raw_data_path, "affiliations.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        affiliation = new_affiliation()

        for line in tqdm(
            f_in,
            desc="Parsing affiliations",
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

            if affiliation["id"] != id:
                if affiliation["id"] != "":
                    f_out.write(json.dumps(affiliation) + "\n")
                    affiliation = new_affiliation()
                affiliation["id"] = id

            if "name" in predicate:
                affiliation["name"] = normalize_str(predicate.split('"')[1])

        f_out.write(json.dumps(affiliation) + "\n")


if __name__ == "__main__":
    main()
