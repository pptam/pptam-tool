#!/usr/bin/env python3.7

import os
import json
import shutil
import argparse
import logging
from os import path
from tools import replace_values_in_file


def debug_prepare_deploy(configuration_file_path, input_file_path, output_file_path):
    if not path.exists(configuration_file_path):
        logging.fatal(f"Cannot find the configuration file {configuration_file_path}.")
        quit()

    with open(configuration_file_path, "r") as f:
        configuration = json.load(f)["Configuration"]

    replacements = []
    for entry in configuration:
        replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configuration[entry]})
        replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": configuration[entry]})

    logging.debug(f"Replacing values.")
    shutil.copyfile(input_file_path, output_file_path)
    replace_values_in_file(output_file_path, replacements)

    logging.info(f"Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates test cases.")
    parser.add_argument("--configuration", metavar="path_to_configuration_file", help="Configuration file", default="configuration.json")
    parser.add_argument("--input", metavar="path_to_yml_input_file", help="Docker compose kinput file", default="docker-compose.yml")
    parser.add_argument("--output", metavar="path_to_yml_output_file", help="Docker compose output file", default="docker-compose.yml")
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    debug_prepare_deploy(args.configuration, args.input, args.output)
