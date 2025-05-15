#!/usr/bin/env python3

import csv
import json
import argparse
import logging

def convert_csv_to_json(csv_filename, output_filename):
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
        cells.append({"src": src, "dest": dest, "values": {"Entity_Dep": 1.0}})

    data = {
        "@schemaVersion": "1.0",
        "name": "Entities",
        "variables": unique_services, 
        "cells": cells
    }

    with open(output_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert entity dependencies CSV to dv8 JSON format.")
    parser.add_argument("input_csv", help="Path to input CSV file.")
    parser.add_argument("output_json", help="Path to output JSON file.")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    convert_csv_to_json(args.input_csv, args.output_json)
