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
        "train",
        "val",
        "test",
    ]:
        split_path = join_path(dataset_path, split)
        read_path = join_path(split_path, "queries.jsonl")
        write_path = join_path(split_path, "query_ids.txt")

        n_queries = count_lines(read_path)

        # Create progress bar
        pbar = tqdm(
            total=n_queries,
            desc=f"Extracting {split} query ids",
            position=0,
            dynamic_ncols=True,
            mininterval=0.5,
        )

        with open(read_path, "r") as f_in, open(write_path, "w") as f_out:
            for line in f_in:
                query_id = json.loads(line)["id"]
                f_out.write(f"{query_id}\n")

                pbar.update(1)

        pbar.close()


if __name__ == "__main__":
    # execute only if run as a script
    main()
