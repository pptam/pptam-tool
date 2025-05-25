#!/usr/bin/env python3

import os
import re
import json
from collections import defaultdict

def extract_proto_fields(proto_file):
    fields = set()
    with open(proto_file, "r") as file:
        content = file.read()
        messages = re.findall(r'message\s+\w+\s*{([^}]*)}', content, re.DOTALL)
        for message in messages:
            matches = re.findall(r'\s*(\w+)\s+(\w+)\s*=\s*\d+;', message)
            for _, field_name in matches:
                fields.add(field_name)
    return fields

def collect_service_fields(services_path):
    service_fields = defaultdict(set)
    for service_name in os.listdir(services_path):
        service_dir = os.path.join(services_path, service_name, "proto")
        if not os.path.isdir(service_dir):
            continue
        for filename in os.listdir(service_dir):
            if filename.endswith(".proto"):
                full_path = os.path.join(service_dir, filename)
                fields = extract_proto_fields(full_path)
                service_fields[service_name].update(fields)
    return service_fields

def find_shared_fields(service_fields):
    shared = []
    services = list(service_fields.keys())
    for i in range(len(services)):
        for j in range(i + 1, len(services)):
            s1, s2 = sorted((services[i], services[j]))  # sort to avoid reverse duplicates
            common = service_fields[s1] & service_fields[s2]
            if common:
                shared.append((s1, s2, sorted(common)))
    return shared

def main():
    with open("parse_import_dependencies.json", "r") as f:
        config = json.load(f)
    services_path = config["services_path"]

    service_fields = collect_service_fields(services_path)
    shared_dependencies = find_shared_fields(service_fields)

    if shared_dependencies:
        with open("data_dependencies.csv", "w", newline="", encoding="utf-8") as f:
            f.write("from;to;fields\n")
            for s1, s2, fields in shared_dependencies:
                field_list = ",".join(fields)
                f.write(f"{s1};{s2};{field_list}\n")

if __name__ == "__main__":
    main()
