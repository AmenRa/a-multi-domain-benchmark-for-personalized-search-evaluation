import bz2
import json
import os

from src.oneliner_utils import join_path
from tqdm import tqdm


def new_paper_references():
    return {
        "doc_id": "",
        "rel_doc_ids": [],
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "08.PaperReferences.nt.bz2")
    write_path = join_path(raw_data_path, "paper_references.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        paper_references = new_paper_references()

        for line in tqdm(
            f_in,
            desc="Parsing paper references",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            parts = line[1:-4].split("> <")
            subject, _, object = parts
            id = subject.split("/")[-1]

            if paper_references["doc_id"] != id:
                if paper_references["doc_id"] != "":
                    f_out.write(json.dumps(paper_references) + "\n")
                    paper_references = new_paper_references()
                paper_references["doc_id"] = id

            paper_references["rel_doc_ids"].append(object.split("/")[-1])

        f_out.write(json.dumps(paper_references) + "\n")


if __name__ == "__main__":
    main()
