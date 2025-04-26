#!/usr/bin/env python3

import argparse
import logging
import csv
import sys
from itertools import combinations
from trainticket_lib import (
    parse_call_dependencies_java,
    parse_call_dependencies_python,
    parse_import_dependencies_java,
    parse_import_dependencies_python,
)

def main():
    parser = argparse.ArgumentParser(description="Parse dependencies for TrainTicket design.")
    parser.add_argument("design_folder", help="Path to the design folder containing JSON files.")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    design_folder = args.design_folder

    logging.info(f"Parsing call dependencies for Java from {design_folder}/parse_call_dependencies_java.json")
    call_dependencies = parse_call_dependencies_java.run_analysis(f"{design_folder}/parse_call_dependencies_java.json")

    logging.info(f"Parsing call dependencies for Python from {design_folder}/parse_call_dependencies_python.json")
    call_dependencies += parse_call_dependencies_python.run_analysis(f"{design_folder}/parse_call_dependencies_python.json")

    call_dependencies = list(map(list, set(map(tuple, call_dependencies))))  # Remove duplicates

    call_csv_path = f"{design_folder}/call_dependencies.csv"
    logging.info(f"Writing call dependencies to {call_csv_path}")
    with open(call_csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["from", "to"])
        for row in call_dependencies:
            writer.writerow(row)

    logging.info(f"Parsing import dependencies for Java from {design_folder}/parse_import_dependencies_java.json")
    import_dependencies = parse_import_dependencies_java.run_analysis(f"{design_folder}/parse_import_dependencies_java.json")

    logging.info(f"Parsing import dependencies for Python from {design_folder}/parse_import_dependencies_python.json")
    import_dependencies += parse_import_dependencies_python.run_analysis(f"{design_folder}/parse_import_dependencies_python.json")

    entity_to_microservices = {}

    for microservice, _, entity in import_dependencies:
        if entity not in entity_to_microservices:
            entity_to_microservices[entity] = set()
        entity_to_microservices[entity].add(microservice)

    call_dependencies = []
    for entity, microservices in entity_to_microservices.items():
        if len(microservices) > 1:
            for combo in combinations(sorted(microservices), 2):
                call_dependencies.append(combo)

    call_dependencies = list(map(list, set(map(tuple, call_dependencies))))  # Remove duplicates

    data_csv_path = f"{design_folder}/data_dependencies.csv"
    logging.info(f"Writing data dependencies to {data_csv_path}")
    with open(data_csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["from", "to"])
        for dep in call_dependencies:
            writer.writerow(dep)

if __name__ == "__main__":
    main()
