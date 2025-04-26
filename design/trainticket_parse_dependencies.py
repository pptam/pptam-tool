#!/usr/bin/env python3

from trainticket_lib import parse_call_dependencies_java
from trainticket_lib import parse_call_dependencies_python
from trainticket_lib import parse_import_dependencies_java
from trainticket_lib import parse_import_dependencies_python
import csv
from itertools import combinations
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python trainticket_parse_dependencies.py <design folder>")
        sys.exit(1)

    design_folder = sys.argv[1]
    call_dependencies = parse_call_dependencies_java.run_analysis(f"{design_folder}/parse_call_dependencies_java.json")
    call_dependencies += (parse_call_dependencies_python.run_analysis(f"{design_folder}/parse_call_dependencies_python.json"))
    call_dependencies = list(map(list, set(map(tuple, call_dependencies)))) # Remove duplicates

    with open(f"{design_folder}/call_dependencies.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["from", "to"])
        for row in call_dependencies:
            writer.writerow(row)

    import_dependencies = parse_import_dependencies_java.run_analysis(f"{design_folder}/parse_import_dependencies_java.json")
    import_dependencies += (parse_import_dependencies_python.run_analysis(f"{design_folder}/parse_import_dependencies_python.json"))

    # Step 1: build a mapping: entity -> set of microservices
    entity_to_microservices = {}

    for microservice, _, entity in import_dependencies:
        if entity not in entity_to_microservices:
            entity_to_microservices[entity] = set()
        entity_to_microservices[entity].add(microservice)

    # Step 2: find combinations
    call_dependencies = []
    for entity, microservices in entity_to_microservices.items():
        if len(microservices) > 1:
            for combo in combinations(sorted(microservices), 2):
                call_dependencies.append(combo)

    call_dependencies = list(map(list, set(map(tuple, call_dependencies)))) # Remove duplicates
    
    with open(f"{design_folder}/data_dependencies.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["from", "to"])
        for dep in call_dependencies:
            writer.writerow(dep)