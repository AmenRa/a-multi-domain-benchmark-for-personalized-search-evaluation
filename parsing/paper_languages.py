import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "PaperLanguages.nt.bz2")
    write_path = join_path(raw_data_path, "paper_languages.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        for line in tqdm(
            f_in,
            desc="Parsing affiliations",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            parts = line[1:-4].split("> <")
            subject, predicate = parts

            lang = {
                "doc_id": subject.split("/")[-1],
                "lang": predicate.split('"')[1],
            }
            f_out.write(json.dumps(lang) + "\n")


if __name__ == "__main__":
    main()
