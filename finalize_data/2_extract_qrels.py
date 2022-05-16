import json

import click
from src.oneliner_utils import count_lines, join_path, write_json
from tqdm import tqdm


@click.command()
@click.option(
    "--lang",
    required=True,
    default="en",
)
@click.option(
    "--fos",
    required=True,
)
def main(lang, fos):
    dataset_path = join_path("datasets", lang, fos)

    for split in [
        "val",
        "test",
    ]:
        split_path = join_path(dataset_path, split)
        read_path = join_path(split_path, "queries.jsonl")
        write_path = join_path(split_path, "qrels.json")

        n_queries = count_lines(read_path)

        # Create progress bar
        pbar = tqdm(
            total=n_queries,
            desc=f"Extracting {split} qrels",
            position=0,
            dynamic_ncols=True,
            mininterval=0.5,
        )

        qrels = {}

        with open(read_path, "r") as f_in:
            for line in f_in:
                query = json.loads(line)

                qrels[query["id"]] = {
                    doc_id: 1 for doc_id in query["rel_doc_ids"]
                }

                pbar.update(1)

        pbar.close()

        write_json(qrels, write_path)

        del qrels


if __name__ == "__main__":
    # execute only if run as a script
    main()
