import random

import click
import optuna
from elasticsearch import Elasticsearch
from optuna.samplers import TPESampler
from ranx import Qrels, Run, evaluate
from src.elasticsearch_utils import msearch, set_bm25
from src.oneliner_utils import join_path, read_jsonl, write_json


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
@click.option(
    "--samples",
    default=5000,
    help="Number of train queries to use for BM25 optimization. Defaults to 5000.",
)
def main(lang, fos, samples):
    random.seed(42)

    dataset_path = join_path("tmp", "datasets", lang, fos)
    final_dataset_path = join_path("datasets", lang, fos)

    train_queries_path = join_path(dataset_path, "train", "queries.jsonl")
    bm25_config_path = join_path(final_dataset_path, "bm25_config.json")

    # Create connection with Elasticsearch
    es_client = Elasticsearch(timeout=180)

    # Load train queries
    train_queries = read_jsonl(train_queries_path)
    # Sample train queries
    train_queries = random.sample(train_queries, samples)

    def objective(trial):
        b = trial.suggest_float("b", 0.0, 1.0, step=0.01)
        k1 = trial.suggest_float("k1", 0.0, 10.0, step=0.1)
        size = 100

        # Set ranking function -------------------------------------------------
        set_bm25(es_client=es_client, index_name="academic-search", b=b, k1=k1)

        # Querying -------------------------------------------------------------
        results = msearch(
            es_client=es_client,
            index_name="academic-search",
            queries=train_queries,
            size=size,
        )

        # Build qrels and run --------------------------------------------------
        qrels = Qrels.from_dict(
            {q["id"]: {r: 1 for r in q["rel_doc_ids"]} for q in train_queries}
        )
        run = Run.from_dict(
            {
                train_queries[i]["id"]: {r[0]: r[1] for r in res}
                for i, res in enumerate(results)
            }
        )

        # Evaluate run ---------------------------------------------------------
        return evaluate(qrels, run, "ndcg@100")

    # Make the sampler behave in a deterministic way.
    sampler = TPESampler(seed=42)
    study = optuna.create_study(sampler=sampler, direction="maximize")
    study.optimize(objective, n_trials=35)

    # Save BM25 config
    write_json(study.best_params, bm25_config_path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
