import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def new_conference_instance():
    return {
        "id": "",
        "name": "",
        "conference_series_id": "",
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "03.ConferenceInstances.nt.bz2")
    write_path = join_path(raw_data_path, "conference_instances.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        conference_instance = new_conference_instance()

        for line in tqdm(
            f_in,
            desc="Parsing conference_instances",
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

            if conference_instance["id"] != id:
                if conference_instance["id"] != "":
                    f_out.write(json.dumps(conference_instance) + "\n")
                    conference_instance = new_conference_instance()
                conference_instance["id"] = id

            if "name" in predicate:
                conference_instance["name"] = normalize_str(
                    predicate.split('"')[1]
                )
            elif "isPartOf" in predicate:
                conference_instance["conference_series_id"] = object.split("/")[
                    -1
                ]

        f_out.write(json.dumps(conference_instance) + "\n")


if __name__ == "__main__":
    main()
