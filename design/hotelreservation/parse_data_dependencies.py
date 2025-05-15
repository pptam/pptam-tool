#!/usr/bin/env python3

import os
import re
from collections import defaultdict

services_path = "./DeathStarBench/hotelReservation/services"  # Root directory containing all service folders

def extract_proto_fields(proto_file):
    fields = set()
    with open(proto_file, "r") as file:
        content = file.read()
        messages = re.findall(r'message\s+\w+\s*{([^}]*)}', content, re.DOTALL)
        for message in messages:
            matches = re.findall(r'\s*(\w+)\s+(\w+)\s*=\s*\d+;', message)
            for field_type, field_name in matches:
                fields.add((field_type, field_name))
    return fields

def collect_service_fields():
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
    shared = defaultdict(set)
    services = list(service_fields.keys())
    for i in range(len(services)):
        for j in range(i + 1, len(services)):
            s1, s2 = services[i], services[j]
            common = service_fields[s1] & service_fields[s2]
            if common:
                shared[(s1, s2)] = common
    return shared

def main():
    service_fields = collect_service_fields()
    shared = find_shared_fields(service_fields)

    for (s1, s2), fields in shared.items():
        print(f"\nShared fields between {s1} and {s2}:")
        for field_type, field_name in fields:
            print(f"  {field_type} {field_name}")

if __name__ == "__main__":
    main()
