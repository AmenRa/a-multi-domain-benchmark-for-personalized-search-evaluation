import json
from multiprocessing import Pool

import click
from src.oneliner_utils import join_path, read_jsonl, read_list
from tqdm import tqdm

fos_id_dict = {
    "history": "95457728",
    "biology": "86803240",
    "medicine": "71924100",
    "computer_science": "41008148",
    "environmental_science": "39432304",
    "mathematics": "33923547",
    "geography": "205649164",
    "materials_science": "192562407",
    "chemistry": "185592680",
    "political_science": "17744445",
    "economics": "162324750",
    "psychology": "15744967",
    "business": "144133560",
    "sociology": "144024400",
    "art": "142362112",
    "philosophy": "138885662",
    "engineering": "127413603",
    "geology": "127313418",
    "physics": "121332964",
}


def get_paper_fos(lang: str, fos: str, prog_bar_position: int):
    # Folder paths
    raw_data_path = join_path("tmp", "raw_data")
    datasets_path = join_path("tmp", "datasets")
    lang_path = join_path(datasets_path, lang)
    dataset_path = join_path(lang_path, fos)

    # File paths
    fos_path = join_path(raw_data_path, "fields_of_study.jsonl")
    doc_ids_path = join_path(dataset_path, "final_doc_ids.txt")
    paper_fos_path = join_path(raw_data_path, "paper_fields_of_study.jsonl")
    write_path = join_path(dataset_path, "paper_fos.jsonl")

    discipline_id = fos_id_dict[fos]
    fos_dict = {x["id"]: x for x in read_jsonl(fos_path)}
    doc_ids = set(read_list(doc_ids_path))

    with open(paper_fos_path, "r") as paper_fos_f, open(
        write_path, "w"
    ) as f_out:
        for line in tqdm(
            paper_fos_f,
            mininterval=1.0,
            desc=fos,
            dynamic_ncols=True,
            position=prog_bar_position,
        ):
            paper_fos = json.loads(line)
            doc_fos_id = paper_fos["fos_id"]
            fos_id = fos_dict[doc_fos_id]["level_0"]

            if fos_id == discipline_id and paper_fos["doc_id"] in doc_ids:
                f_out.write(line.strip() + "\n")


@click.command()
@click.argument("fos_list", nargs=-1)
@click.option("--lang", default="en")
def main(lang, fos_list):
    with Pool(len(fos_list)) as pool:
        pool.starmap(
            get_paper_fos,
            [(lang, fos, i) for i, fos in enumerate(fos_list)],
        )


if __name__ == "__main__":
    main()
