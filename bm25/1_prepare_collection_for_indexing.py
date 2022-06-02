import json
from multiprocessing import Pool

import click
from src.oneliner_utils import count_lines, join_path
from src.preprocessing import preprocessing
from tqdm import tqdm


def prepare_document(doc):
    doc = json.loads(doc)
    doc = {
        "id": doc["id"],
        "contents": preprocessing(doc["title"] + "\n" + doc["text"]),
        "timestamp": doc["timestamp"],
    }
    doc["timestamp"] = max(doc["timestamp"], 0)

    return doc


def prepare_collection(lang, fos, threads):
    read_path = join_path("datasets", lang, fos, "collection.jsonl")
    write_path = join_path(
        "tmp", "datasets", lang, fos, "bm25_collection.jsonl"
    )

    n_lines = count_lines(read_path)
    chunk_size = 100
    remaining_lines = n_lines

    # Create progress bar
    pbar = tqdm(
        total=n_lines,
        desc=f"{fos} - preparing documents for indexing",
        position=0,
        dynamic_ncols=True,
        mininterval=0.5,
    )

    with open(read_path, "r") as f_in, open(write_path, "w") as f_out, Pool(
        threads
    ) as p:
        while remaining_lines > 0:
            # Read lines chunk
            chunk = [
                f_in.readline() for _ in range(min(chunk_size, remaining_lines))
            ]

            docs = p.map(prepare_document, chunk)

            for x in docs:
                f_out.write(f"{json.dumps(x)}\n")

            # Update remaining lines counter
            remaining_lines -= len(chunk)

            pbar.update(len(chunk))

        p.close()
        p.join()


@click.command()
@click.option("--lang", required=True, default="en")
@click.option("--fos", required=True)
@click.option(
    "--threads",
    required=True,
    default=4,
    help="Number of threads to use. Defaults to 4.",
)
def main(lang, fos, threads):
    prepare_collection(lang, fos, threads)


if __name__ == "__main__":
    # execute only if run as a script
    main()
