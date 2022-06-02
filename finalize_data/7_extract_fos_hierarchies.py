import click
from src.oneliner_utils import join_path, read_jsonl, write_jsonl

level_0_fos = {
    "95457728",  # History
    "86803240",  # Biology
    "71924100",  # Medicine
    "41008148",  # Computer science
    "39432304",  # Environmental scie
    "33923547",  # Mathematics
    "205649164",  # Geography
    "192562407",  # Materials science
    "185592680",  # Chemistry
    "17744445",  # Political science
    "162324750",  # Economics
    "15744967",  # Psychology
    "144133560",  # Business
    "144024400",  # Sociology
    "142362112",  # Art
    "138885662",  # Philosophy
    "127413603",  # Engineering
    "127313418",  # Geology
    "121332964",  # Physics
}


def get_fos_hierarchy(parent_id, fos_children_dict):
    if (
        parent_id is None
        or parent_id not in fos_children_dict
        or parent_id in level_0_fos
    ):
        return None

    parent_of_the_parent_id = get_fos_hierarchy(
        fos_children_dict[parent_id], fos_children_dict
    )

    if parent_of_the_parent_id is None:
        return [parent_id]

    return parent_of_the_parent_id + [parent_id]


def get_fos_hierarachies(fos_children_dict):
    fos_list = [{"id": k} for k in fos_children_dict]

    for fos in fos_list:
        if fos["id"] in fos_children_dict:
            fos["hierarchy"] = get_fos_hierarchy(fos["id"], fos_children_dict)
        elif fos["id"] in level_0_fos:
            fos["hierarchy"] = fos["id"]
        else:
            # fos["hierarchy"] = None
            print(fos)
            exit()

    return [
        {"fos_id": fos["id"], "hierarchy": fos["hierarchy"]}
        for fos in fos_list
        if fos["hierarchy"]
    ]


@click.command()
@click.option("--fos", required=True)
@click.option("--lang", required=True, default="en")
def main(lang, fos):
    # Folder paths
    raw_data_path = join_path("tmp", "raw_data")
    # dataset_path = join_path("tmp", "datasets", lang, fos)
    final_dataset_path = join_path("datasets", lang, fos)

    # File paths
    fos_children_path = join_path(
        raw_data_path, "field_of_study_children.jsonl"
    )
    collection_path = join_path(final_dataset_path, "collection.jsonl")

    print("Loading collection")
    collection = read_jsonl(collection_path)
    fos_list = {x for doc in collection for x in doc["fields_of_study"]}

    print("Loading FoS relations data")
    fos_children_dict = {
        x["id"]: x["parent"]
        for x in read_jsonl(fos_children_path)
        if x["id"] in fos_list
    }

    print("Getting FoS hierarchies")
    fos_hierarachies = get_fos_hierarachies(fos_children_dict)

    print("Saving FoS hierarchies")
    write_jsonl(
        fos_hierarachies,
        join_path(final_dataset_path, "fos_hierarachies.jsonl"),
    )


if __name__ == "__main__":
    # execute only if run as a script
    main()
