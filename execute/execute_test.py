#!/usr/bin/env python3.7

import os
import time
import argparse
import logging
import time
import shutil
import configparser
import datetime
import requests
import threading

from lib import run_external_applicaton, replace_values_in_file


def perform_test(configuration, section, repetition):
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
        logging.warning(f"Skipping test {test_id_without_timestamp}, since it already exists.")
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

    try:
        if os.path.exists(deployment_descriptor):
            command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} {test_id}"
            run_external_applicaton(command_deploy_stack)
            logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
            time.sleep(seconds_to_wait_for_deployment)

        host = configuration["DEFAULT"]["locust_host_url"]
        load = configuration["DEFAULT"]["load"]
        hatch_rate = configuration["DEFAULT"]["hatch_rate_per_second"]
        run_time = configuration["DEFAULT"]["run_time_in_seconds"]
        log_file = os.path.splitext(driver)[0] + ".log"
        out_file = os.path.splitext(driver)[0] + ".out"
        csv_prefix = os.path.join(os.path.dirname(driver), "result")
        logging.info(f"Running the load test for {test_id}.")
        run_external_applicaton(f'locust --locustfile {driver} --host {host} --users {load} --hatch-rate {hatch_rate} --run-time {run_time}s --headless --only-summary --csv {csv_prefix} --csv-full-history --logfile "{log_file}" >> {out_file} 2> {out_file}', False)

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


def execute_test(design_path):
    configuration = configparser.ConfigParser()
    configuration.read([os.path.join(design_path, "configuration.ini"), os.path.join(design_path, "test_plan.ini")])

    for section in configuration.sections():
        if section.lower().startswith("test"):
            enabled = (configuration[section]["enabled"] == "1")
            if enabled:
                repeat = int(configuration[section]["repeat"])
                for repetition in range(repeat):
                    perform_test(configuration, section, repetition)

    logging.info(f"Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("--design", metavar="path_to_design_folder", help="Design folder", default="../design")
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)

    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)

    design_path = args.design
    if not os.path.exists(design_path):
        logging.fatal(f"Cannot find the design folder {design_path}.")
        quit()

    execute_test(design_path)
