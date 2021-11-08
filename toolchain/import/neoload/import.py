#!/usr/bin/env python3

import argparse
import logging
import configparser
import os
import shutil
import pandas
from datetime import datetime
import math


def get_line(key, rows):
    request_type = ""
    name = key
    request_count: int = rows["Element"].count()
    failure_count = rows["Errors"].sum()

    median_response_time = rows["Median duration"].median()
    average_response_time = rows["Average duration"].mean()
    min_response_time = rows["Minimum duration"].min()
    max_response_time = rows["Maximum duration"].max()
    requests_per_second = rows["Elements/s"].mean()
    failures_per_second = rows["Errors/s"].mean()
    standard_deviation = rows["Median duration"].std()

    return f"{request_type},{name},{request_count},{failure_count},{median_response_time},{average_response_time}," \
            f"{min_response_time},{max_response_time},{requests_per_second},{failures_per_second},{standard_deviation}"

def create_output_directory(all_outputs, test_id_without_timestamp, timestamp):
    test_id = timestamp.strftime("%Y%m%d%H%M%S") + "-" + test_id_without_timestamp

    if any(x.endswith(test_id_without_timestamp) for x in os.listdir(all_outputs)):
        name_of_existing_folder = next(x for x in os.listdir(all_outputs) if x.endswith(test_id_without_timestamp))
        logging.warning(f"Deleting {name_of_existing_folder}, since it already exists.")
        shutil.rmtree(os.path.join(all_outputs, name_of_existing_folder))

    output = os.path.join(all_outputs, test_id)
    os.makedirs(output)

    return output, test_id
    
def convert(input, project, test_set, test, timestamp, load):
    all_outputs = os.path.abspath(os.path.join("../../executed"))
    if not os.path.isdir(all_outputs):
        logging.debug(f"Creating {all_outputs}, since it does not exist.")
        os.makedirs(all_outputs)
    
    data_frame = pandas.read_csv(input, sep=";")
    data_frame = data_frame.drop(data_frame[data_frame.Element == "<all requests>"].index)

    initial_test_id_without_timestamp = test_set + "-" + test
    test_id_without_timestamp = f"{initial_test_id_without_timestamp}-{load}"
    timestamp_in_millis = timestamp.timestamp()
    output, test_id = create_output_directory(all_outputs, test_id_without_timestamp, timestamp)
    logging.debug(f"Importing data from {input} and storing it into the folder {output}...")

    configuration = configparser.ConfigParser()
    configuration.optionxform=str
    configuration.add_section("CONFIGURATION")
    configuration.set("CONFIGURATION", "PROJECT_NAME", project)
    configuration.set("CONFIGURATION", "TEST_SET_NAME", test_set)
    configuration.set("CONFIGURATION", "TEST_NAME", test)
    configuration.set("CONFIGURATION", "LOAD", str(load))
    configuration.set("CONFIGURATION", "TIMESTAMP", str(timestamp_in_millis))
    with open(os.path.join(output, "configuration.ini"), "w") as configfile:
        configuration.write(configfile, space_around_delimiters=False)
    
    groups = {}
    group_names = data_frame.groupby(["Element"]).groups.keys()
    for group_name in group_names:
        groups[group_name] = data_frame[data_frame["Element"] == group_name]
    
    header = "Type,Name,Request Count,Failure Count,Median Response Time,Average Response Time,Min Response Time,Max Response Time,Requests/s,Failures/s,Standard Deviation Response Time"

    with open(os.path.join(output, "results.csv"), "w") as results:
        results.write(f"{header}\n")
        for key, value in groups.items():
            results.write(f"{get_line(key, value)}\n")

        aggregated_data = get_line("Aggregated", data_frame)
        results.write(f"{aggregated_data}\n")

def valid_timestamp(s):
    try:
        return datetime.strptime(s, "%Y%m%d%H%M%S")
    except ValueError:
        raise argparse.ArgumentTypeError("not a valid timestamp: '{0}'.".format(s))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Imports results from NeoLoad.")
    parser.add_argument("input", help="jtl file to import")
    parser.add_argument("project", help="Name of the project")    
    parser.add_argument("testset", help="Name of the test set")
    parser.add_argument("test", help="Name of the test")
    parser.add_argument("timestamp", help="Timestamp using the format YYYYMMDDhhmmss, e.g., 2021013115400", type=valid_timestamp)
    parser.add_argument("load", type=int, help="Load that is connected to the imported data")

    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)
        
    convert(args.input, args.project, args.testset, args.test, args.timestamp, args.load)
