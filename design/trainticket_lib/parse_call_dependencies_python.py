#!/usr/bin/env python3

import os
import re
import json

def extract_service_dependencies(root_dir, subfolders):
    pattern = re.compile(r'http://(ts-[a-zA-Z0-9\-]+-service)')
    service_names = {}

    for subfolder in subfolders:
        full_path = os.path.abspath(os.path.join(root_dir, subfolder))
        print(f"Analyzing folder {full_path}...")
        for dirpath, _, filenames in os.walk(full_path):
            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.readlines()
                            for line in content:
                                if line.lstrip().startswith("//"):
                                    continue
                                matches = pattern.findall(line)
                                if matches:
                                    if subfolder not in service_names:
                                        service_names[subfolder] = []
                                    service_names[subfolder].extend(matches)
                    except Exception:
                        pass

    return service_names

def run_analysis(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    root_folder = config["root_folder"]
    subfolders_to_traverse = config["subfolders_to_traverse"]

    results = extract_service_dependencies(root_folder, subfolders_to_traverse)

    lines = []
    for subfolder in sorted(results.keys()):
        for service in sorted(set(results[subfolder])):
            lines.append([subfolder, service])

    return lines

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parse_call_dependencies_python.py <config_file.json>")
        sys.exit(1)
    for line in run_analysis(sys.argv[1]):
        print(";".join(line))
