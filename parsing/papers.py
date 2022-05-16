import bz2
import json
import os

from src.oneliner_utils import join_path
from src.string_normalization import normalize_str
from src.to_timestamp import date_to_timestamp
from tqdm import tqdm


def new_paper():
    return {
        "id": "",
        "title": "",
        "conference_instance_id": "",
        "conference_series_id": "",
        "journal_id": "",
        "cit_count": "",
        "estimated_cit_count": "",
        "ref_count": "",
        "issue_id": "",
        "volume": "",
        "publisher": "",
        "doi": "",
        "publication_date": "",
        "timestamp": "",
    }


def main():
    archives_path = join_path("tmp", "archives")
    raw_data_path = join_path("tmp", "raw_data")
    read_path = join_path(archives_path, "10.Papers.nt.bz2")
    write_path = join_path(raw_data_path, "papers.jsonl")
    os.makedirs(raw_data_path, exist_ok=True)

    with bz2.open(read_path, "rt") as f_in, open(write_path, "w") as f_out:
        paper = new_paper()

        for line in tqdm(
            f_in,
            desc="Parsing papers",
            mininterval=1.0,
            position=0,
            dynamic_ncols=True,
        ):
            try:
                parts = line[:-4].split("> <")

                if len(parts) == 3:
                    subject, predicate, object = parts
                else:
                    subject, predicate = parts

                id = subject.split("/")[-1]

                if paper["id"] != id:
                    if paper["id"] != "":
                        f_out.write(json.dumps(paper) + "\n")
                        paper = new_paper()
                    paper["id"] = id

                if "appearsInConferenceInstance" in predicate:
                    paper["conference_instance_id"] = object.split("/")[-1]
                if "appearsInConferenceSeries" in predicate:
                    paper["conference_series_id"] = object.split("/")[-1]
                elif "appearsInJournal" in predicate:
                    paper["journal_id"] = object.split("/")[-1]
                elif "citationCount" in predicate:
                    paper["cit_count"] = int(predicate.split('"')[1])
                elif "estimatedCitationCount" in predicate:
                    paper["estimated_cit_count"] = int(predicate.split('"')[1])
                elif "referenceCount" in predicate:
                    paper["ref_count"] = int(predicate.split('"')[1])
                elif "publicationDate" in predicate:
                    paper["publication_date"] = predicate.split('"')[1]
                    paper["timestamp"] = date_to_timestamp(
                        paper["publication_date"]
                    )
                elif "issueIdentifier" in predicate:
                    paper["issue_id"] = predicate.split('"')[1]
                elif "volume" in predicate:
                    paper["volume"] = predicate.split('"')[1]
                elif "publisher" in predicate:
                    try:
                        paper["publisher"] = normalize_str(
                            predicate.split('"')[1]
                        )
                    except:
                        paper["publisher"] = " ".join(
                            object.split("/")[-1].split("_")
                        )
                elif "title" in predicate:
                    paper["title"] = normalize_str(predicate.split('"')[1])
                elif "doi" in predicate:
                    paper["doi"] = predicate.split('"')[1]

            except Exception as e:
                print(e)
                print(line)
                print(parts)
                exit()

        f_out.write(json.dumps(paper) + "\n")


if __name__ == "__main__":
    main()
