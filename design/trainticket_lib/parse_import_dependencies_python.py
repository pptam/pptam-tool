#!/usr/bin/env python3

import json

def run_analysis(config_file):
    with open(config_file, "r") as f:
        config = json.load(f)

    hard_coded_result = config["hard_coded_results"]

    return [hard_coded_result]


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parse_import_dependencies_python.py <config_file.json>")
        sys.exit(1)
    for line in run_analysis(sys.argv[1]):
        print(";".join(line))

