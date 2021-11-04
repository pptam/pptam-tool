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

    # Assumes that labels have the form of NAME-REQUEST_TYPE
    if "-" in key:
        request_type = key.split("-")[1].upper()
    
    name = key
    request_count: int = rows["label"].count()
    failure_count = rows[~rows["success"]]["label"].count()
    median_response_time = rows["elapsed"].median()
    average_response_time = rows["elapsed"].mean()
    min_response_time = rows["elapsed"].min()
    max_response_time = rows["elapsed"].max()
    min_ts: int = rows["timeStamp"].min()
    max_ts: int = rows["timeStamp"].max()
    duration: int = int((max_ts - min_ts)/1000)
    average_content_size_recv = rows["bytes"].mean()
    average_content_size_sent = rows["sentBytes"].mean()
    requests_per_second = request_count/duration
    failures_per_second = failure_count/duration
    percentile_25 = rows["elapsed"].quantile(q=0.25)
    percentile_50 = rows["elapsed"].quantile(q=0.5)
    percentile_75 = rows["elapsed"].quantile(q=0.75)
    percentile_80 = rows["elapsed"].quantile(q=0.8)
    percentile_90 = rows["elapsed"].quantile(q=0.9)
    percentile_95 = rows["elapsed"].quantile(q=0.95)
    percentile_98 = rows["elapsed"].quantile(q=0.98)
    percentile_99 = rows["elapsed"].quantile(q=0.99)
    percentile_99_9 = rows["elapsed"].quantile(q=0.999)
    percentile_99_99 = rows["elapsed"].quantile(q=0.9999)
    percentile_100 = rows["elapsed"].quantile(q=1)
    standard_deviation = rows["elapsed"].std()

    return f"{request_type},{name},{request_count},{failure_count},{median_response_time},{average_response_time}," \
            f"{min_response_time},{max_response_time},{average_content_size_recv},{requests_per_second}," \
            f"{failures_per_second},{percentile_25},{percentile_50},{percentile_75},{percentile_80},{percentile_90}," \
            f"{percentile_95},{percentile_98},{percentile_99},{percentile_99_9},{percentile_99_99},{percentile_100}," \
            f"{standard_deviation}"

def create_output_directory(all_outputs, test_id_without_timestamp, timestamp):
    test_id = timestamp.strftime("%Y%m%d%H%M") + "-" + test_id_without_timestamp

    if any(x.endswith(test_id_without_timestamp) for x in os.listdir(all_outputs)):
        name_of_existing_folder = next(x for x in os.listdir(all_outputs) if x.endswith(test_id_without_timestamp))
        logging.warning(f"Deleting {name_of_existing_folder}, since it already exists.")
        shutil.rmtree(os.path.join(all_outputs, name_of_existing_folder))

    output = os.path.join(all_outputs, test_id)
    os.makedirs(output)

    return output, test_id
    
def convert(input, project, test_set, test, load):
    all_outputs = os.path.abspath(os.path.join("../../executed"))
    
    data_frame = pandas.read_csv(input)
    test_id_without_timestamp = f"{test_set}-{test}-{load}"
    timestamp_in_millis = math.trunc(data_frame.iloc[0]["timeStamp"]/1000)
    timestamp = datetime.fromtimestamp(timestamp_in_millis)
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

    # Inspired by https://github.com/radon-h2020/demo-ctt-todolistapi/tree/main/jmeter/experiment/03_PPTAM_Import/jmeter-to-pptam by Thomas F. Duellmann       
    groups = {}
    group_names = data_frame.groupby(["label"]).groups.keys()
    for group_name in group_names:
            groups[group_name] = data_frame[data_frame["label"] == group_name]
    
    header = "Type,Name,Request Count,Failure Count,Median Response Time,Average Response Time,Min Response Time,Max Response Time,Average Content Size,Requests/s,Failures/s,25%,50%,75%,80%,90%,95%,98%,99%,99.9%,99.99%,100%,Standard Deviation Response Time"

    with open(os.path.join(output, "results.csv"), "w") as results:
        results.write(f"{header}\n")
        for key, value in groups.items():
            results.write(f"{get_line(key, value)}\n")

        aggregated_data = get_line("Aggregated", data_frame)
        results.write(f"{aggregated_data}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Imports results from JMeter.")
    parser.add_argument("input", help="jtl file to import")
    parser.add_argument("project", help="Name of the project")    
    parser.add_argument("testset", help="Name of the test set")
    parser.add_argument("test", help="Name of the test")
    parser.add_argument("load", type=int, help="Load that is connected to the imported data")

    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)
        
    convert(args.input, args.project, args.testset, args.test, args.load)
