#!/usr/bin/env python3

import argparse
import logging
import csv
import os
from itertools import combinations
import parse_call_dependencies

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse dependencies.")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    call_dependencies = []
    logging.info("Parsing call dependencies from ./parse_call_dependencies.json")
    call_dependencies += parse_call_dependencies.run_analysis("./parse_call_dependencies.json")

    call_dependencies = list(map(list, set(map(tuple, call_dependencies))))  # Remove duplicates

    call_csv_path = "./call_dependencies.csv"
    logging.info(f"Writing call dependencies to {call_csv_path}")
    with open(call_csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["from", "to"])
        for row in call_dependencies:
            writer.writerow(row)