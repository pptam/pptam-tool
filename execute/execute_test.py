#!/usr/bin/env python3.7

import os
import time
import argparse
import logging
from os import path
import json
import sys
from time import sleep
import subprocess
import shutil


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = "=" * filled_len + "-" * (bar_len - filled_len)
    sys.stdout.write("[%s] %s%s %s\r" % (bar, percents, '%', suffix))
    sys.stdout.flush()


def run_external_applicaton(command, fail_if_result_not_zero=True):
    logging.debug(f"Executing {command}.")
    result = os.system(command)
    if fail_if_result_not_zero and result != 0:
        logging.fatal(f"Could not execute {command}.")
        raise RuntimeError


def execute_test(configuration_file_path):
    if not path.exists(configuration_file_path):
        logging.fatal(f"Cannot find the configuration file {configuration_file_path}.")
        raise RuntimeError

    with open(configuration_file_path, "r") as f:
        configuration = json.load(f)["Configuration"]

    input = path.abspath(configuration["test_case_to_execute_folder"])
    if not path.isdir(input):
        logging.fatal(f"Cannot find the test case folder {input}.")
        raise RuntimeError
    else:
        logging.debug(f"Executing test cases from {input}.")

    seconds_to_wait_for_deployment = int(configuration["test_case_waiting_for_deployment_in_seconds"])
    time_to_complete_one_test = seconds_to_wait_for_deployment + (((int(configuration["test_case_ramp_up_in_seconds"]) + int(configuration["test_case_steady_state_in_seconds"]) + int(configuration["test_case_ramp_down_in_seconds"])) // 60) + 1) * 60
    time_to_complete_all_tests = len([name for name in os.listdir(f"{input}/") if os.path.isdir(name)]) * time_to_complete_one_test
    logging.info(f"Estimated duration of ONE test: {time_to_complete_one_test} seconds.")
    logging.info(f"Estimated duration of ALL tests: {time_to_complete_all_tests} seconds.")

    output = path.abspath(configuration["test_case_executed_folder"])
    logging.debug(f"Storing results in {output}.")

    faban_master = f"http://{configuration['faban_ip']}:9980/"
    faban_client = path.abspath("./faban/benchflow-faban-client/target/benchflow-faban-client.jar")

    command_to_execute_before_a_test = configuration["pre_exec_external_command"]
    command_to_execute_after_a_test = configuration["post_exec_external_command"]
    command_to_execute_at_a_test = configuration["on_exec_external_command"]

    for f in os.scandir(input):
        if (path.isdir(f)):
            try:
                logging.info(f"Executing test case {f.name}.")

                if (len(command_to_execute_before_a_test) > 0):
                    run_external_applicaton(command_to_execute_before_a_test)

                test_id = f.name
                temporary_file = f"{test_id}.tmp"

                test_output_path = f"{output}/{test_id}"
                if path.isdir(test_output_path):
                    logging.info(f"Removing path {test_output_path} since it already exists.")
                    shutil.rmtree(path, ignore_errors=False, onerror=RuntimeError)
                else:
                    os.makedirs(test_output_path)

                deployment_descriptor = f"{input}/{test_id}/docker-compose.yml"
                command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} {test_id}"

                run_external_applicaton(command_deploy_stack)

                logging.debug(f"Waiting for {seconds_to_wait_for_deployment} seconds.")
                time_elapsed = 0
                wait(seconds_to_wait_for_deployment, time_to_complete_one_test, "Waiting for deployment.", time_elapsed)
                time_elapsed = seconds_to_wait_for_deployment

                driver = f"{input}/{test_id}/{test_id}.jar"
                driver_configuration = f"{input}/{test_id}/run.xml"
                command_deploy_faban = f"java -jar {faban_client} {faban_master} deploy {test_id} {driver} {driver_configuration} > {temporary_file}"

                run_external_applicaton(command_deploy_faban)

                with open(temporary_file, "r") as f:
                    std_out_deploy_faban = f.readline().rstrip()
                run_id = std_out_deploy_faban
                logging.debug(f"Obtained {run_id} as run ID.")
                os.remove(temporary_file)

                status = ""
                external_tool_was_started = False

                while ((status != "COMPLETED") and (status != "FAILED")):
                    command_status_faban = f"java -jar {faban_client} {faban_master} status {run_id} > {temporary_file}"

                    run_external_applicaton(command_status_faban)

                    with open(temporary_file, "r") as f:
                        std_out_status_faban = f.readline().rstrip()
                    status = std_out_status_faban
                    os.remove(temporary_file)
                    logging.debug(f"Current Faban status: {status}.")

                    if (status == "STARTED" and external_tool_was_started == False and len(command_to_execute_before_a_test) > 0):
                        external_tool_was_started = True
                        run_external_applicaton(command_to_execute_at_a_test)

                    if ((status != "COMPLETED") and (status != "FAILED")):
                        if time_elapsed < time_to_complete_one_test:
                            wait_until = 60
                        else:
                            wait_until = 10

                        logging.debug(f"Waiting for {wait_until} seconds.")
                        wait(wait_until, time_to_complete_one_test, "Waiting for deployment.", time_elapsed)
                        time_elapsed += wait_until

                progress(time_to_complete_one_test, time_to_complete_one_test, "\n")
                if (len(command_to_execute_after_a_test) > 0):
                    run_external_applicaton(command_to_execute_after_a_test)
            finally:
                command_undeploy_stack = f"docker stack rm {test_id}"
                run_external_applicaton(command_undeploy_stack, False)

                if path.isfile(temporary_file):
                    os.remove(temporary_file)

            if (status == "COMPLETED"):
                logging.info(f"Saving test results into {test_output_path}.")
                shutil.move(f"./faban/output/{run_id}", f"{test_output_path}/faban")
                shutil.move(f"{input}/{test_id}", f"{test_output_path}/definition")

                command_info_faban = f"java -jar {faban_client} {faban_master} info {run_id} > {test_output_path}/faban/runInfo.txt"
                run_external_applicaton(command_info_faban)


def wait(seconds_to_wait_for_deployment, time_to_complete_one_test, information, time_already_elapsed):
    count = 0
    while count < seconds_to_wait_for_deployment:
        progress(time_already_elapsed + count, time_to_complete_one_test, str(count))
        count += 1
        sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("--configuration", metavar="path_to_configuration_file", help="Configuration file", default="configuration.json")
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    execute_test(args.configuration)
