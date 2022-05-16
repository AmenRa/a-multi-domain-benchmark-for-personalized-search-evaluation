import bz2
import json
import os

from src.oneliner_utils import join_path
from tqdm import tqdm


def new_paper_authors():
    return {
        "doc_id": "",
        "author_ids": [],
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "06.PaperAuthorAffiliations.nt.bz2")
    write_path = join_path(raw_data_path, "paper_authors.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        paper_authors = new_paper_authors()

        for line in tqdm(
            f_in,
            desc="Parsing paper-author affiliations",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            parts = line[1:-4].split("> <")
            subject, _, object = parts
            id = object.split("/")[-1]

            if paper_authors["doc_id"] != id:
                if paper_authors["doc_id"] != "":
                    f_out.write(json.dumps(paper_authors) + "\n")
                    paper_authors = new_paper_authors()
                paper_authors["doc_id"] = id

            paper_authors["author_ids"].append(subject.split("/")[-1])

        f_out.write(json.dumps(paper_authors) + "\n")


if __name__ == "__main__":
    main()
