import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl
from src.to_timestamp import year_to_timestamp


@click.command()
@click.option("--fos", required=True)
@click.option("--lang", default="en")
@click.option("--year", default=2019)
def main(lang, fos, year):
    print(f"{fos} : Filtering test docs")
    dataset_path = join_path("datasets", lang, fos)
    collection_path = join_path(dataset_path, "collection.jsonl")

    timestamp = year_to_timestamp(year)

    docs = read_jsonl(collection_path)
    print(len(docs))
    docs = [d for d in docs if d["timestamp"] < timestamp]
    print(len(docs))
    write_jsonl(docs, collection_path)


if __name__ == "__main__":
    main()
