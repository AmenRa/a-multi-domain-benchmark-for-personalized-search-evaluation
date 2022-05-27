import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from tqdm import tqdm


def new_paper_tags():
    return {
        "doc_id": "",
        "keywords": [],
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "21.PaperTags.nt.bz2")
    write_path = join_path(raw_data_path, "paper_tags.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        paper_tags = new_paper_tags()

        for line in tqdm(
            f_in,
            desc="Parsing paper-tags",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            parts = line[1:-4].split("> <")
            subject, predicate = parts
            id = subject.split("/")[-1]

            if paper_tags["doc_id"] != id:
                if paper_tags["doc_id"] != "":
                    f_out.write(json.dumps(paper_tags) + "\n")
                    paper_tags = new_paper_tags()
                paper_tags["doc_id"] = id

            keyword = normalize_str(predicate.split('"')[1])
            if keyword not in paper_tags["keywords"]:
                paper_tags["keywords"].append(keyword)

        f_out.write(json.dumps(paper_tags) + "\n")


if __name__ == "__main__":
    main()
