#!/usr/bin/env python3

import os
import re
import json
import argparse
import logging

def extract_grpc_calls(root_dir, subfolders):
    grpc_pattern = re.compile(r's\.getGprcConn\(')
    func_pattern = re.compile(r'^\s*func\s*(?:\(.*?\))?\s*(\w+)\s*\(')

    service_calls = {}

    for subfolder in subfolders:
        full_path = os.path.abspath(os.path.join(root_dir, subfolder))
        logging.info(f"Analyzing folder {full_path}...")
        for dirpath, _, filenames in os.walk(full_path):
            for filename in filenames:
                if filename.endswith(".go"):
                    file_path = os.path.join(dirpath, filename)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            current_function = None
                            for line in file:
                                # Update current function if we find a new one
                                func_match = func_pattern.match(line)
                                if func_match:
                                    current_function = func_match.group(1)
                    
                                if grpc_pattern.search(line):
                                    if subfolder not in service_calls:
                                        service_calls[subfolder] = []
                                    if current_function:
                                        cleaned_function = current_function
                                        if cleaned_function.startswith("init"):
                                            cleaned_function = cleaned_function[4:]  # Remove 'init'
                                        if cleaned_function.endswith("Client"):
                                            cleaned_function = cleaned_function[:-6]  # Remove 'Client'
                                        service_calls[subfolder].append(cleaned_function)
                                    else:
                                        service_calls[subfolder].append("(no function)")

                    except Exception as e:
                        logging.error(f"Failed to process file {file_path}: {e}")

    return service_calls

def run_analysis(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    root_folder = config["root_folder"]
    subfolders_to_traverse = config["subfolders_to_traverse"]

    results = extract_grpc_calls(root_folder, subfolders_to_traverse)

    lines = []
    for subfolder in sorted(results.keys()):
        for func in sorted(set(results[subfolder])):
            lines.append([subfolder, func])

    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse functions using s.getGrpcConn from Go source files.")
    parser.add_argument("config_file", help="Path to the configuration JSON file.")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    for line in run_analysis(args.config_file):
        print(";".join(line))
