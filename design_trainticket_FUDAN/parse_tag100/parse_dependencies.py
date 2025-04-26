import parse_call_dependencies_java
import parse_call_dependencies_python
import parse_data_dependencies_java
import parse_data_dependencies_python
import csv
from itertools import combinations


def get_pairwise_shared_entities(results):
    entity_to_services = {}

    # Step 1: Build a map from entity to the services that import it
    for service, entities in results.items():
        for entity in entities:
            entity_to_services.setdefault(entity, set()).add(service)

    # Step 2: Generate all unique service pairs per entity
    pairwise_combos = []
    for entity, services in entity_to_services.items():
        if len(services) >= 2:
            for service1, service2 in combinations(sorted(services), 2):
                pairwise_combos.append([service1, service2, entity])
    return pairwise_combos


if __name__ == "__main__":
    call_dependencies = parse_call_dependencies_java.main()
    call_dependencies += parse_call_dependencies_python.main()

    with open("call_dependencies.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["from", "to"])
        for row in call_dependencies:
            writer.writerow(row)

    data_dependencies = parse_data_dependencies_java.main()
    data_dependencies.update(parse_data_dependencies_python.main())

    pairwise_data_dependencies = get_pairwise_shared_entities(data_dependencies)
    with open("data_dependencies.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["from", "to", "entity"])
        for row in pairwise_data_dependencies:
            writer.writerow(row)
