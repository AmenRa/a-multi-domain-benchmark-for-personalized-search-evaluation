import bz2
import json
import os

from src.oneliner_utils import join_path
from tqdm import tqdm


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "19.PaperCitationContexts.nt.bz2")
    write_path = join_path(raw_data_path, "citation_contexts.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        for line in tqdm(
            f_in,
            desc="Parsing citation contexts",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            parts = line[1:-4].split("> <")

            try:
                if len(parts) == 3:
                    subject, predicate, object = parts
                else:
                    subject, predicate = parts

                if "hasContext" in predicate:
                    id = subject.split("/")[-1]
                    citation_context = {
                        "citing_id": id.split("-")[0],
                        "cited_id": id.split("-")[1],
                        "context": predicate.split('"')[1],
                    }
                    f_out.write(json.dumps(citation_context) + "\n")
            except:
                print(line)
                exit()


if __name__ == "__main__":
    main()
