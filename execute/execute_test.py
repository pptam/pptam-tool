#!/usr/bin/env python3.8

import os
import time
import argparse
import logging
import shutil
import configparser
import datetime
import requests
import threading
import docker
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import csv

from lib import run_external_applicaton, replace_values_in_file


def flatten_hierarchy(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def get_docker_stats(client, bucket, org, write_api, test_case_name):
    for container in client.containers.list():
        stats = container.stats(stream=False)

        data = {"tags": {}, "fields": {}}
        data["measurement"] = "docker_stats"
        data["time"] = stats["read"]
        data["tags"]["test_case_name"] = test_case_name
        data["tags"]["container_name"] = container.name
        print(stats)

        record = Point.from_dict(data)
        print(record.to_line_protocol())
        write_api.write(bucket, org, record)

    time.sleep(60)
    get_docker_stats(client, bucket, org, write_api, test_case_name)


def perform_test(configuration, section, repetition, overwrite_existing_results):
    logging.debug(f"Checking if InfluxDB is up...")
    try:
        response = requests.get(url=configuration[section]["influxdb_url"] + "/health")
        data = response.json()
        if data["status"] != "pass":
            logging.fatal(f"InfluxDB health check was not successful.")
            raise SystemExit()

        logging.debug(f"Checking if InfluxDB is up...")
    except requests.exceptions.RequestException:  # This is the correct syntax
        logging.fatal(f"InfluxDB is down, please start it before executing tests.")
        raise SystemExit()

    command_to_execute_before_a_test = configuration["DEFAULT"]["pre_exec_external_command"]
    command_to_execute_after_a_test = configuration["DEFAULT"]["post_exec_external_command"]
    command_to_execute_at_a_test = configuration["DEFAULT"]["on_exec_external_command"]

    now = datetime.datetime.now()
    test_id_without_timestamp = configuration[section]["test_case_prefix"].lower() + "-" + section.lower() + "-" + str(repetition + 1)
    test_id = now.strftime("%Y%m%d%H%M%S") + "-" + test_id_without_timestamp

    all_outputs = os.path.abspath(os.path.join("./executed"))
    if not os.path.isdir(all_outputs):
        logging.debug(f"Creating {all_outputs}, since it does not exist.")
        os.makedirs(all_outputs)
    if any(x.endswith(test_id_without_timestamp) for x in os.listdir(all_outputs)):
        if overwrite_existing_results:
            name_of_existing_folder = next(x for x in os.listdir(all_outputs) if x.endswith(test_id_without_timestamp))
            logging.warning(f"Deleting {name_of_existing_folder}, since it already exists and the --override flag is set.")
            shutil.rmtree(os.path.join(all_outputs, name_of_existing_folder))
        else:
            logging.warning(f"Skipping test {test_id_without_timestamp}, since it already exists. Use --overwrite in case.")
            return

    output = os.path.join(all_outputs, test_id)
    os.makedirs(output)

    deployment_descriptor = f"{output}/docker-compose.yml"
    driver = f"{output}/locustfile.py"

    logging.debug(f"Creating a folder name {test_id} in {output}.")
    if os.path.exists(os.path.join(design_path, "docker-compose.yml")):
        shutil.copyfile(os.path.join(design_path, "docker-compose.yml"), deployment_descriptor)
    shutil.copyfile(os.path.join(design_path, "locustfile.py"), driver)

    replacements = []
    for entry in configuration[section].keys():
        replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configuration[section][entry]})
        replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": configuration[section][entry]})

    replacements.append({"search_for": "${TEST_NAME}", "replace_with": test_id})

    logging.debug(f"Replacing values.")
    if os.path.exists(deployment_descriptor):
        replace_values_in_file(deployment_descriptor, replacements)
    replace_values_in_file(driver, replacements)

    with open(os.path.join(output, "configuration.txt"), "w") as f:
        for option in configuration.options(section):
            f.write(f"{option}={configuration[section][option]}\n")

    logging.info(f"Executing test case {test_id}.")

    if (len(command_to_execute_before_a_test) > 0):
        run_external_applicaton(f"{command_to_execute_before_a_test}")

    seconds_to_wait_for_deployment = int(configuration["DEFAULT"]["test_case_waiting_for_deployment_in_seconds"])
    seconds_to_wait_for_undeployment = int(configuration["DEFAULT"]["test_case_waiting_for_undeployment_in_seconds"])

    sut_hostname = configuration["DEFAULT"]["docker_sut_hostname"]
    docker_client = docker.DockerClient(base_url=f"{sut_hostname}:2375")

    token = configuration[section]["influxdb_token"]
    org = configuration[section]["influxdb_organization"]
    bucket = configuration[section]["influxdb_bucket"]
    client = InfluxDBClient(url=configuration[section]["influxdb_url"], token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    try:
        if os.path.exists(deployment_descriptor):
            command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} {test_id}"
            run_external_applicaton(command_deploy_stack)
            logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
            time.sleep(seconds_to_wait_for_deployment)

        run_docker_stats_in_background = threading.Thread(target=get_docker_stats, args=(
            docker_client,
            bucket,
            org,
            write_api,
            test_id_without_timestamp,
        ), daemon=True)
        run_docker_stats_in_background.start()

        host = configuration["DEFAULT"]["locust_host_url"]
        load = configuration["DEFAULT"]["load"]
        spawn_rate = configuration["DEFAULT"]["spawn_rate_per_second"]
        run_time = configuration["DEFAULT"]["run_time_in_seconds"]
        log_file = os.path.splitext(driver)[0] + ".log"
        out_file = os.path.splitext(driver)[0] + ".out"
        csv_prefix = os.path.join(os.path.dirname(driver), "result")
        logging.info(f"Running the load test for {test_id}, with {load} users, running for {run_time} seconds.")
        run_external_applicaton(f'locust --locustfile {driver} --host {host} --users {load} --spawn-rate {spawn_rate} --run-time {run_time}s --headless --only-summary --csv {csv_prefix} --csv-full-history --logfile "{log_file}" >> {out_file} 2> {out_file}', False)

        if len(command_to_execute_at_a_test) > 0:
            run_external_applicaton(f"{command_to_execute_at_a_test}")

        if (len(command_to_execute_after_a_test) > 0):
            run_external_applicaton(f"{command_to_execute_after_a_test}")
    finally:
        if os.path.exists(deployment_descriptor):
            command_undeploy_stack = f"docker stack rm {test_id}"
            run_external_applicaton(command_undeploy_stack, False)
            logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
            time.sleep(seconds_to_wait_for_undeployment)

    logging.info(f"Test {test_id} completed. Test results can be found in {output}.")

    with open(os.path.join(output, "result_stats.csv"), "r") as f1:
        reader = csv.DictReader(f1)
        for row in reader:
            data = {"tags": {}, "fields": {}}
            data["tags"]["test_case_name"] = test_id_without_timestamp
            data["tags"]["type"] = row["Type"]
            data["tags"]["name"] = row["Name"]
            data["fields"]["request_count"] = int(row["Request Count"])
            data["fields"]["failure_count"] = int(row["Failure Count"])
            data["fields"]["median_response_time"] = float(row["Median Response Time"])
            data["fields"]["average_response_time"] = float(row["Average Response Time"])
            data["fields"]["min_response_time"] = float(row["Min Response Time"])
            data["fields"]["max_response_time"] = float(row["Max Response Time"])
            data["fields"]["average_content_size"] = float(row["Average Content Size"])
            data["fields"]["requests_per_second"] = float(row["Requests/s"])
            data["fields"]["failures_per_second"] = float(row["Failures/s"])
            for i in ["50%", "66%", "75%", "80%", "90%", "95%", "98%", "99%", "99.9%", "99.99%", "100%"]:
                if row[i] != "N/A":
                    data["fields"]["percentile_" + i[:-1]] = float(row[i])

            if row["Name"] != "Aggregated":
                data["measurement"] = "response_time"
                data["tags"]["type"] = row["Type"]
                data["tags"]["name"] = row["Name"]
            else:
                data["measurement"] = "response_time_aggregated"

            record = Point.from_dict(data)
            write_api.write(bucket, org, record)

    with open(os.path.join(output, "result_stats_history.csv"), "r") as f2:
        reader = csv.DictReader(f2)
        for row in reader:
            data = {"tags": {}, "fields": {}}
            data["time"] = datetime.datetime.fromtimestamp(int(row["Timestamp"]))
            data["tags"]["test_case_name"] = test_id_without_timestamp
            data["tags"]["type"] = row["Type"]
            data["tags"]["name"] = row["Name"]
            data["fields"]["currently_running_users"] = int(row["User Count"])
            data["fields"]["total_request_count"] = int(row["Total Request Count"])
            data["fields"]["total_failure_count"] = int(row["Total Failure Count"])
            data["fields"]["total_median_response_time"] = float(row["Total Median Response Time"])
            data["fields"]["total_average_response_time"] = float(row["Total Average Response Time"])
            data["fields"]["total_min_response_time"] = float(row["Total Min Response Time"])
            data["fields"]["total_max_response_time"] = float(row["Total Max Response Time"])
            data["fields"]["total_average_content_size"] = float(row["Total Average Content Size"])
            data["fields"]["requests_per_second"] = float(row["Requests/s"])
            data["fields"]["failures_per_second"] = float(row["Failures/s"])
            for i in ["50%", "66%", "75%", "80%", "90%", "95%", "98%", "99%", "99.9%", "99.99%", "100%"]:
                if row[i] != "N/A":
                    data["fields"]["percentile_" + i[:-1]] = float(row[i])

            if row["Name"] != "Aggregated":
                data["measurement"] = "response_time_history"
                data["tags"]["type"] = row["Type"]
                data["tags"]["name"] = row["Name"]
            else:
                data["measurement"] = "response_time_history_aggregated"

            record = Point.from_dict(data)
            write_api.write(bucket, org, record)

    with open(os.path.join(output, "result_failures.csv"), "r") as f3:
        reader = csv.DictReader(f3)
        for row in reader:
            data = {"tags": {}, "fields": {}}
            data["tags"]["test_case_name"] = test_id_without_timestamp
            data["tags"]["type"] = row["Method"]
            data["tags"]["name"] = row["Name"]
            data["fields"]["error"] = row["Error"]
            data["fields"]["occurrences"] = int(row["Occurrences"])
            data["measurement"] = "failures"

            record = Point.from_dict(data)
            write_api.write(bucket, org, record)


def execute_test(design_path, overwrite_existing_results):
    configuration = configparser.ConfigParser()
    configuration.read([os.path.join(design_path, "configuration.ini"), os.path.join(design_path, "test_plan.ini")])

    for section in configuration.sections():
        if section.lower().startswith("test"):
            enabled = (configuration[section]["enabled"] == "1")
            if enabled:
                repeat = int(configuration[section]["repeat"])
                for repetition in range(repeat):
                    perform_test(configuration, section, repetition, overwrite_existing_results)

    logging.info(f"Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("--design", metavar="path_to_design_folder", help="Design folder")
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)
    parser.add_argument("--overwrite", help="Overwrite existing test cases", action='store_true', default=False)

    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)

    design_path = args.design
    if design_path == None or (not os.path.exists(design_path)):
        logging.fatal(f"Cannot find the design folder. Please indicate one with the parameter --design")
        quit()

    execute_test(design_path, args.overwrite)
