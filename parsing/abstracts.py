import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "PaperAbstracts.nt.bz2")
    write_path = join_path(raw_data_path, "abstracts.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        line = ""

        for l in tqdm(
            f_in,
            desc="Parsing abstracts",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            line += f"{l.strip()} "
            if "<http://www.w3.org/2001/XMLSchema#string> ." in line:
                parts = line.strip()[1:-4].split("> <")
                subject, predicate = parts

                abstract = {
                    "doc_id": subject.split("/")[-1],
                    "text": normalize_str(predicate.split('"')[1]),
                }
                f_out.write(json.dumps(abstract) + "\n")

                line = ""

        f_out.write(json.dumps(abstract) + "\n")


if __name__ == "__main__":
    main()
