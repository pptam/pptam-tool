#!/usr/bin/env python3.7

import json
import sys
import argparse
from configparser import ConfigParser
import logging

parser = argparse.ArgumentParser(description="Converts ini files to json.")
parser.add_argument("--input", metavar="ini_file", help="The file path of the ini file to read.", default="configuration.ini")
parser.add_argument("--output", metavar="json_file", help="The file path of the json file to write.", default="configuration.json")
parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)    
args = parser.parse_args()

logging.basicConfig(format='%(message)s', level=args.logging * 10)   

with open(args.input, "r") as f:
    configuration = ConfigParser()
    configuration.read_file(f)

result = {}

for section in configuration.sections():
    result[section] = {}
    for name, value in configuration.items(section):
        result[section][name] = [x.strip() for x in value.split() if x]
        if len(result[section][name]) == 1:
            result[section][name] = result[section][name][0]
        elif len(result[section][name]) == 0:
            result[section][name] = ''

with open(args.output, "w") as f:
    f.writelines(json.dumps(result, indent=2))

logging.info(f"Configuration was written to the file {args.output}.")
