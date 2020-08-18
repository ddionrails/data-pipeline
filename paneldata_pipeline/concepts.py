""" Data manipulation functionality related to the concepts.csv."""
import csv
from pathlib import Path
from typing import Set


def extract_implicit_concepts(input_path: Path, concepts_path: Path = Path()) -> None:
    """Add missing concepts, only in variables and questions data, to concepts.csv"""
    if concepts_path == Path():
        concepts_path = input_path.joinpath("concepts.csv")

    implicit_concepts: Set[str] = set()

    for path in [
        input_path.joinpath("variables.csv"),
        input_path.joinpath("questions.csv"),
    ]:
        with open(path, "r") as csv_file:
            for row in csv.DictReader(csv_file):
                _concept = row.get("concept", row.get("concept_name"))
                if _concept is None:
                    raise EnvironmentError(
                        f"{concepts_path} is missing the 'concept' field."
                    )
                implicit_concepts.add(_concept)

    if not concepts_path.exists():
        with open(concepts_path, "w+") as concepts_csv:
            csv.DictWriter(
                concepts_csv, fieldnames=["name", "topic", "label_de", "label"]
            ).writeheader()

    with open(concepts_path, "r") as concepts_csv:
        concepts_reader = csv.DictReader(concepts_csv)
        concept_csv_content = list(concepts_reader)
        if concepts_reader.fieldnames:
            concept_fields = {name: "" for name in concepts_reader.fieldnames}
        else:
            raise EnvironmentError(f"{concepts_path} is not a correct concept CSV file.")
        explicit_concepts = {row["name"] for row in concept_csv_content}

    implicit_concepts.difference_update(explicit_concepts)
    if "" in implicit_concepts:
        implicit_concepts.remove("")
    with open(concepts_path, "w") as concepts_csv:
        writer = csv.DictWriter(concepts_csv, concept_fields.keys())
        writer.writeheader()
        for row in concept_csv_content:
            writer.writerow(row)
        for concept in implicit_concepts:
            concept_fields["name"] = concept
            writer.writerow(concept_fields)
