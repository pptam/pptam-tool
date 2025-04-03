import csv
import json
import sys

def convert_csv_to_json(csv_filename):
    services = set()
    connections = []

    with open(csv_filename, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            services.add(row['from'])
            services.add(row['to'])
            connections.append((row['from'], row['to']))

    unique_services = list(services)
    service_to_index = {service: index for index, service in enumerate(unique_services)}

    cells = []
    for connection in connections:
        src = service_to_index[connection[0]]
        dest = service_to_index[connection[1]]
        cells.append({"src": src, "dest": dest, "values": {"Call": 1.0}})

    data = {
        "@schemaVersion": "1.0",
        "name": "ServiceCalls",
        "variables": unique_services,
        "cells": cells
    }

    with open('service_calls.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert2dv8.py <input_csv_file>")
        sys.exit(1)

    convert_csv_to_json(sys.argv[1])
