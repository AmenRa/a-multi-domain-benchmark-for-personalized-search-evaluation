import json

import click
from elasticsearch import Elasticsearch
from src.elasticsearch_utils import msearch, set_bm25
from src.oneliner_utils import count_lines, join_path, read_json
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
    # Folder paths
    dataset_path = join_path("tmp", "datasets", lang, fos)
    final_dataset_path = join_path("datasets", lang, fos)

    # Create connection with Elasticsearch
    es_client = Elasticsearch(timeout=180)

    # Load bm25 config
    bm25_config_path = join_path(final_dataset_path, "bm25_config.json")
    bm25_config = read_json(bm25_config_path)

    # Set BM25 config
    set_bm25(es_client=es_client, index_name="academic-search", **bm25_config)

    # Querying -----------------------------------------------------------------
    for split in [
        "train",
        "test",
    ]:
        read_path = join_path(dataset_path, split, "queries.jsonl")
        write_path = join_path(dataset_path, split, "bm25_queries.jsonl")

        n_queries = count_lines(read_path)

        # Create progress bar
        pbar = tqdm(
            total=n_queries,
            desc=f"{fos} - Running {split} queries",
            position=0,
            dynamic_ncols=True,
            mininterval=0.5,
        )

        size = 100 if split == "train" else 1000

        with open(read_path, "r") as f_in, open(write_path, "w") as f_out:
            chunk = []
            chunk_size = 100

            for i, line in enumerate(f_in):
                chunk.append(json.loads(line))

                if (i + 1) % chunk_size == 0 or (i + 1) == n_queries:
                    # Run queries ----------------------------------------------
                    results = msearch(
                        es_client=es_client,
                        index_name="academic-search",
                        queries=chunk,
                        size=size,
                        show_progress=False,
                    )

                    # Update queries -------------------------------------------
                    for j in range(len(chunk)):
                        # Add BM25 result list ---------------------------------
                        chunk[j]["bm25_doc_ids"] = [x[0] for x in results[j]]
                        chunk[j]["bm25_doc_scores"] = [x[1] for x in results[j]]

                        # Clean relevant list ----------------------------------
                        chunk[j]["rel_doc_ids"] = sorted(
                            [
                                x
                                for x in chunk[j]["rel_doc_ids"]
                                if x in chunk[j]["bm25_doc_ids"]
                            ]
                        )

                    # Remove queries with no relevants retrieved ---------------
                    queries = [x for x in chunk if len(x["rel_doc_ids"]) > 0]

                    # Remove queries with less than 10 results retrieved by BM25
                    queries = [
                        x for x in queries if len(x["bm25_doc_ids"]) >= 10
                    ]

                    # Write queries --------------------------------------------
                    f_out.write(
                        "\n".join(json.dumps(x) for x in queries) + "\n"
                    )

                    pbar.update(len(chunk))
                    chunk = []

            # Sanity check
            assert not chunk, "Error: chunk is not empty"

        pbar.close()


if __name__ == "__main__":
    # execute only if run as a script
    main()
