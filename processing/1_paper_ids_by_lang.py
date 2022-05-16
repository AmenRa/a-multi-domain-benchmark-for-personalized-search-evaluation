import json
import os

from src.oneliner_utils import join_path, write_list
from tqdm import tqdm

# fmt: off
lang_list = ["dv", "mt", "sw", "ur", "de", "sr", "km", "ka", "ku", "si", "bg", "ps", "be", "ca", "af", "zh_cht", "nl", "sl", "fr", "tl", "ml", "ht", "sq", "ta", "da", "lo", "sk", "ja", "ko", "it", "iu", "uk", "en", "so", "tr", "ar", "hu", "uz", "is", "vi", "hr", "eo", "hy", "chr", "eu", "kn", "ru", "lv", "ga", "or", "cy", "fa", "sv", "fi", "lt", "my", "he", "et", "el", "no", "la", "mk", "pt", "nn", "pl", "th", "id", "te", "es", "ro", "gl", "yi", "pa", "ms", "gu", "bn", "hi", "cs", "zh_chs"]
# fmt: on


def main():
    raw_data_path = join_path("tmp", "raw_data")
    doc_ids_by_lang_path = join_path(raw_data_path, "lang")
    os.makedirs(doc_ids_by_lang_path, exist_ok=True)

    langs_path = join_path(raw_data_path, "paper_languages.jsonl")

    lang_doc_ids_dict = {x: [] for x in lang_list}

    with open(langs_path, "r") as lang_f:
        for line in tqdm(
            lang_f,
            mininterval=1.0,
            desc="Dividing doc ids by lang",
            dynamic_ncols=True,
        ):
            lang = json.loads(line)
            lang_doc_ids_dict[lang["lang"]].append(lang["doc_id"])

    for k, v in lang_doc_ids_dict.items():
        write_list(v, join_path(doc_ids_by_lang_path, f"{k}_doc_ids.txt"))


if __name__ == "__main__":
    main()
