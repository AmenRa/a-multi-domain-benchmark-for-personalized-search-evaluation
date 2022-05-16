from src.oneliner_utils import join_path, read_jsonl, write_jsonl

level_0_fos = {
    "95457728",  # History
    "86803240",  # Biology
    "71924100",  # Medicine
    "41008148",  # Computer science
    "39432304",  # Environmental science
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


def get_level_0_fos(parent_id, fos_children_dict):
    if parent_id in fos_children_dict:
        return get_level_0_fos(fos_children_dict[parent_id], fos_children_dict)
    else:
        return parent_id if parent_id in level_0_fos else None


def main():
    raw_data_path = join_path("tmp", "raw_data")
    fos_path = join_path(raw_data_path, "fields_of_study.jsonl")
    fos_children_path = join_path(
        raw_data_path, "field_of_study_children.jsonl"
    )

    print("Load data")
    fos_list = read_jsonl(fos_path)
    fos_children_list = read_jsonl(fos_children_path)
    fos_children_dict = {x["id"]: x["parent"] for x in fos_children_list}

    print("Get level 0 fos")
    for fos in fos_list:
        if fos["id"] in fos_children_dict:
            fos["level_0"] = get_level_0_fos(fos["id"], fos_children_dict)
        elif fos["id"] in level_0_fos:
            fos["level_0"] = fos["id"]
        else:
            fos["level_0"] = None

    print("Update fields_of_study.jsonl")
    write_jsonl(fos_list, fos_path)


if __name__ == "__main__":
    main()
