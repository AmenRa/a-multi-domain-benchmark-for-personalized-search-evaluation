import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl


@click.command()
@click.option("--fos", required=True)
@click.option("--lang", required=True, default="en")
def main(lang, fos):
    raw_data_path = join_path("tmp", "raw_data")
    dataset_path = join_path("datasets", lang, fos)

    collection_path = join_path(dataset_path, "collection.jsonl")

    conference_instances_path = join_path(
        raw_data_path, "conference_instances.jsonl"
    )
    conference_series_path = join_path(raw_data_path, "conference_series.jsonl")
    journals_path = join_path(raw_data_path, "journals.jsonl")

    print("Loading collection")
    docs = read_jsonl(collection_path)

    print("Loading conference instances")
    conference_instances = read_jsonl(conference_instances_path)

    print("Loading conference series")
    conference_series = read_jsonl(conference_series_path)

    print("Loading journals")
    journals = read_jsonl(journals_path)

    conference_instance_ids = {
        d["conference_instance_id"]
        for d in docs
        if len(d["conference_instance_id"]) > 0
    }

    conference_series_ids = {
        d["conference_series_id"]
        for d in docs
        if len(d["conference_series_id"]) > 0
    }

    journal_ids = {d["journal_id"] for d in docs if len(d["journal_id"]) > 0}

    conference_instances = [
        x for x in conference_instances if x["id"] in conference_instance_ids
    ]
    conference_series = [
        x for x in conference_series if x["id"] in conference_series_ids
    ]
    journals = [x for x in journals if x["id"] in journal_ids]

    print("Saving data")
    write_jsonl(
        conference_instances,
        join_path(dataset_path, "conference_instances.jsonl"),
    )
    write_jsonl(
        conference_series, join_path(dataset_path, "conference_series.jsonl")
    )
    write_jsonl(journals, join_path(dataset_path, "journals.jsonl"))


if __name__ == "__main__":
    # execute only if run as a script
    main()
