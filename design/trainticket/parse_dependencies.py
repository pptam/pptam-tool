#!/usr/bin/env python3

import argparse
import logging
import csv
import os
from itertools import combinations
from lib import (
    parse_call_dependencies_java,
    parse_call_dependencies_python,
    parse_import_dependencies_java,
    parse_import_dependencies_python,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse dependencies.")
    parser.add_argument("design_folder", help="Path to the design folder containing JSON files.")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    design_folder = args.design_folder

    if any(os.path.isfile(f"{design_folder}/{fname}") for fname in ["parse_call_dependencies_java.json", "parse_call_dependencies_python.json"]):
        call_dependencies = []
        if os.path.isfile(f"{design_folder}/parse_call_dependencies_java.json"):
            logging.info(f"Parsing call dependencies from {design_folder}/parse_call_dependencies_java.json")
            call_dependencies += parse_call_dependencies_java.run_analysis(f"{design_folder}/parse_call_dependencies_java.json")

        if os.path.isfile(f"{design_folder}/parse_call_dependencies_python.json"):
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

    if any(os.path.isfile(f"{design_folder}/{fname}") for fname in ["parse_import_dependencies_java.json", "parse_import_dependencies_python.json"]):
        import_dependencies = []
        if os.path.isfile(f"{design_folder}/parse_import_dependencies_java.json"):
            logging.info(f"Parsing import dependencies from {design_folder}/parse_import_dependencies_java.json")
            import_dependencies += parse_import_dependencies_java.run_analysis(f"{design_folder}/parse_import_dependencies_java.json")

        if os.path.isfile(f"{design_folder}/parse_import_dependencies_python.json"):
            logging.info(f"Parsing import dependencies for Python from {design_folder}/parse_import_dependencies_python.json")
            import_dependencies += parse_import_dependencies_python.run_analysis(f"{design_folder}/parse_import_dependencies_python.json")

        entity_to_microservices = {}

        import_csv_path = f"{design_folder}/import_dependencies.csv"
        with open(import_csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["microservice", "source", "entity"])

            for microservice, source, entity in import_dependencies:
                writer.writerow([microservice, source, entity])
                logging.info(f"Found import dependency in {microservice}, from {source} to {entity}")
                if entity not in entity_to_microservices:
                    entity_to_microservices[entity] = set()
                entity_to_microservices[entity].add(microservice)

        data_dependencies = []
        for entity, microservices in entity_to_microservices.items():
            if len(microservices) > 1:
                for combo in combinations(sorted(microservices), 2):
                    data_dependencies.append(combo)

        data_dependencies = list(map(list, set(map(tuple, data_dependencies))))  # Remove duplicates

        data_csv_path = f"{design_folder}/data_dependencies.csv"
        logging.info(f"Writing data dependencies to {data_csv_path}")
        with open(data_csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["from", "to"])
            for dep in data_dependencies:
                writer.writerow(dep)