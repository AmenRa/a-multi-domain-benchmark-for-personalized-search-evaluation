import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def new_conference_serie():
    return {
        "id": "",
        "name": "",
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "04.ConferenceSeries.nt.bz2")
    write_path = join_path(raw_data_path, "conference_series.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        conference_serie = new_conference_serie()

        for line in tqdm(
            f_in,
            desc="Parsing conference_series",
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

            if conference_serie["id"] != id:
                if conference_serie["id"] != "":
                    f_out.write(json.dumps(conference_serie) + "\n")
                    conference_serie = new_conference_serie()
                conference_serie["id"] = id

            if "name" in predicate:
                conference_serie["name"] = normalize_str(
                    predicate.split('"')[1]
                )

        f_out.write(json.dumps(conference_serie) + "\n")


if __name__ == "__main__":
    main()
