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

from lib import progress, run_external_applicaton, wait, replace_values_in_file


def get_load_testing_state():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    session.headers.update({"Content-Type": "application/json"})
    try:
        response = session.get("http://localhost:8089/stats/requests")
        response_as_json = json.loads(response.content)
        return response_as_json["state"]
    except:
        return "stopped"


def run_locust(host, users, hatch_rate, run_time):
    # Consider using https://github.com/locustio/locust/issues/222
    run_external_applicaton(f"locust --host {host} --users {users} --hatch-rate {hatch_rate} --run-time {run_time}s --headless")


def perform_test(configuration, section, repetition):
    command_to_execute_before_a_test = configuration["DEFAULT"]["pre_exec_external_command"]
    command_to_execute_after_a_test = configuration["DEFAULT"]["post_exec_external_command"]
    command_to_execute_at_a_test = configuration["DEFAULT"]["on_exec_external_command"]

    now = datetime.datetime.now()
    test_id_without_timestamp = configuration[section]["test_case_prefix"].lower() + "-" + section.lower() + "-" + str(repetition + 1)
    test_id = now.strftime("%Y%m%d%H%M%S") + "-" + test_id_without_timestamp
    if any(x.endswith(test_id_without_timestamp) for x in os.listdir(os.path.join("./", configuration["DEFAULT"]["test_case_creation_folder"]))):
        logging.warning(f"Skipping test {test_id_without_timestamp}, since it already exists.")
        return

    output = os.path.abspath(os.path.join("./", configuration["DEFAULT"]["test_case_creation_folder"]), test_id)
    os.makedirs(output)

    logging.debug(f"Generating a test with the id {test_id} in {output}.")
    shutil.copyfile(os.path.join(design_path, "docker-compose.yml"), os.path.join(output, "docker-compose.yml"))
    shutil.copyfile(os.path.join(design_path, "locustfile.py"), os.path.join(output, "locustfile.py"))

    replacements = []
    for entry in configuration[section].keys():
        replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configuration[section][entry]})
        replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": configuration[section][entry]})

    replacements.append({"search_for": "${TEST_NAME}", "replace_with": test_id})

    logging.debug(f"Replacing values.")
    replace_values_in_file(os.path.join(output, "docker-compose.yml"), replacements)
    replace_values_in_file(os.path.join(output, "locustfile.py"), replacements)

    with open(os.path.join(output, "configuration.txt"), "w") as f:
        for option in configuration.options(section):
            f.write(f"{option}={configuration[section][option]}\n")

    logging.info(f"Executing test case {test_id}.")

    if (len(command_to_execute_before_a_test) > 0):
        run_external_applicaton(f"{command_to_execute_before_a_test}")

    test_output_path = f"{output}/{test_id}"
    deployment_descriptor = f"{test_output_path}/docker-compose.yml"
    command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} {test_id}"
    seconds_to_wait_for_deployment = int(configuration["DEFAULT"]["test_case_waiting_for_deployment_in_seconds"])
    seconds_to_wait_for_undeployment = int(configuration["DEFAULT"]["test_case_waiting_for_undeployment_in_seconds"])
    time_to_complete_one_test = seconds_to_wait_for_deployment + seconds_to_wait_for_undeployment + (((int(configuration["DEFAULT"]["test_case_ramp_up_in_seconds"]) + int(configuration["DEFAULT"]["test_case_steady_state_in_seconds"]) + int(configuration["DEFAULT"]["test_case_ramp_down_in_seconds"])) // 60) + 1) * 60

    try:
        run_external_applicaton(command_deploy_stack)

        logging.debug(f"Waiting for {seconds_to_wait_for_deployment} seconds.")
        wait(seconds_to_wait_for_deployment, time_to_complete_one_test, "Waiting for deployment.", 0)
        time_elapsed = seconds_to_wait_for_deployment

        host = configuration["DEFAULT"]["sut_url"]
        load = configuration["DEFAULT"]["load"]
        hatch_rate = configuration["DEFAULT"]["hatch_rate"]
        run_time = configuration["DEFAULT"]["run_time_in_seconds"]
        load_testing = threading.Thread(target=run_locust, args=(host, load, hatch_rate, run_time))
        load_testing.start()

        time.sleep(1)
        while True:
            state = get_load_testing_state()

            if state != "stopped" and external_tool_was_started == False and len(command_to_execute_at_a_test) > 0:
                external_tool_was_started = True
                run_external_applicaton(f"{command_to_execute_at_a_test}")

            if state != "stopped":
                if time_elapsed < time_to_complete_one_test:
                    wait_until = 60
                else:
                    wait_until = 10

                logging.debug(f"Waiting for {wait_until} seconds.")
                wait(wait_until, time_to_complete_one_test, f"Waiting for test to finish ({state}).", time_elapsed, time_to_complete_one_test - seconds_to_wait_for_undeployment)
                time_elapsed += wait_until

            if state == "stopped":
                break

        if (len(command_to_execute_after_a_test) > 0):
            run_external_applicaton(f"{command_to_execute_after_a_test}")
    finally:
        command_undeploy_stack = f"docker stack rm {test_id}"
        run_external_applicaton(command_undeploy_stack, False)

    logging.debug(f"Waiting for {seconds_to_wait_for_undeployment} seconds.")
    wait(seconds_to_wait_for_undeployment, time_to_complete_one_test, "Waiting for undeployment.            ", time_elapsed)
    progress(time_to_complete_one_test, time_to_complete_one_test, "Done.                                \n")

    logging.info(f"Test {test_id} completed. Test results can be found in {test_output_path}.")


def execute_test(design_path):
    configuration = configparser.ConfigParser()
    configuration.read(os.path.join(design_path, "configuration.ini"))

    input = os.path.abspath(os.path.join("./", configuration["DEFAULT"]["test_case_creation_folder"]))
    if not os.path.isdir(input):
        logging.fatal(f"Cannot find the test case folder {input}.")
        raise RuntimeError
    else:
        logging.debug(f"Executing test cases from {input}.")

    seconds_to_wait_for_deployment = int(configuration["DEFAULT"]["test_case_waiting_for_deployment_in_seconds"])
    seconds_to_wait_for_undeployment = int(configuration["DEFAULT"]["test_case_waiting_for_undeployment_in_seconds"])
    time_to_complete_one_test = seconds_to_wait_for_deployment + seconds_to_wait_for_undeployment + (((int(configuration["DEFAULT"]["test_case_ramp_up_in_seconds"]) + int(configuration["DEFAULT"]["test_case_steady_state_in_seconds"]) + int(configuration["DEFAULT"]["test_case_ramp_down_in_seconds"])) // 60) + 1) * 60
    time_to_complete_all_tests = (len([name for name in os.listdir(f"{input}/") if os.path.isdir(f"{input}/{name}")]) * time_to_complete_one_test // 60) + 1
    logging.info(f"Estimated duration of ONE test: approx. {time_to_complete_one_test} seconds.")
    logging.info(f"Estimated duration of ALL tests: approx. {time_to_complete_all_tests} minutes.")

    output = os.path.abspath(os.path.join("./", configuration["DEFAULT"]["test_case_executed_folder"]))
    logging.debug(f"Storing results in {output}.")

    for section in configuration.sections():
        if section.lower().startswith("test"):
            enabled = (configuration[section]["enabled"] == "1")
            if enabled:
                repeat = int(configuration[section]["repeat"])
                for repetition in range(repeat):
                    perform_test(configuration, section, repetition)


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
