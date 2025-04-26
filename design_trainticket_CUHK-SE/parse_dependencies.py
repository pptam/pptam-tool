#!/usr/bin/env python3

import parse_call_dependencies_java
import parse_call_dependencies_python
import parse_import_dependencies_java
import parse_import_dependencies_python
import csv
from itertools import combinations

if __name__ == "__main__":
    call_dependencies = parse_call_dependencies_java.run_analysis("./parse_call_dependencies_java.json")
    call_dependencies += (parse_call_dependencies_python.run_analysis("./parse_call_dependencies_python.json"))
    call_dependencies = list(map(list, set(map(tuple, call_dependencies)))) # remove duplicates

    with open("call_dependencies.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["from", "to"])
        for row in call_dependencies:
            writer.writerow(row)

    import_dependencies = parse_import_dependencies_java.run_analysis("./parse_import_dependencies_java.json")
    import_dependencies += (parse_import_dependencies_python.run_analysis())
    import_dependencies = list(map(list, set(map(tuple, import_dependencies)))) # remove duplicates

    # Step 1: build a mapping: entity -> set of microservices
    entity_to_microservices = {}

    for microservice, _, entity in import_dependencies:
        if entity not in entity_to_microservices:
            entity_to_microservices[entity] = set()
        entity_to_microservices[entity].add(microservice)

    # Step 2: find combinations
    with open("data_dependencies.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["from", "to"])
        for entity, microservices in entity_to_microservices.items():
            if len(microservices) > 1:
                for combo in combinations(sorted(microservices), 2):
                    writer.writerow(combo)