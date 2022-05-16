import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def new_journal():
    return {
        "id": "",
        "name": "",
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "05.Journals.nt.bz2")
    write_path = join_path(raw_data_path, "journals.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        journal = new_journal()

        for line in tqdm(
            f_in,
            desc="Parsing journals",
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

            if journal["id"] != id:
                if journal["id"] != "":
                    f_out.write(json.dumps(journal) + "\n")
                    journal = new_journal()
                journal["id"] = id

            if "name" in predicate:
                journal["name"] = normalize_str(predicate.split('"')[1])

        f_out.write(json.dumps(journal) + "\n")


if __name__ == "__main__":
    main()
