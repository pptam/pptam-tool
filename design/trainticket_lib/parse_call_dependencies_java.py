#!/usr/bin/env python3

import os
import re
import json
import argparse
import logging

def extract_service_dependencies(root_dir, subfolders):
    pattern = re.compile(r'getServiceUrl\s*\(\s*"([^"]+)"\s*\)')
    service_names = {}

    for subfolder in subfolders:
        full_path = os.path.abspath(os.path.join(root_dir, subfolder))
        logging.info(f"Analyzing folder {full_path}...")
        for dirpath, _, filenames in os.walk(full_path):
            for filename in filenames:
                if filename.endswith("Impl.java"):
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
                    except Exception as e:
                        logging.error(f"Failed to process file {file_path}: {e}")

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
    parser = argparse.ArgumentParser(description="Parse service call dependencies from Java source files.")
    parser.add_argument("config_file", help="Path to the configuration JSON file.")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    for line in run_analysis(args.config_file):
        print(";".join(line))