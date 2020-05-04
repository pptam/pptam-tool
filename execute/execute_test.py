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
    print("[%s] %s%s ...%s\r" % (bar, percents, '%', suffix), flush=True)


def wait(seconds, suffix):
    count = 0
    while count < seconds:
        progress(count, seconds, suffix)
        count += 1
        sleep(1)


def run_external_applicaton(command, information, fail_if_result_not_zero=True):
    logging.info(information)
    logging.debug(f"Executing {command}.")
    result = os.system(command)
    if fail_if_result_not_zero and result != 0:
        logging.fatal(f"Could not execute {command}.")
        raise RuntimeError


def execute_test(configuration_file_path):
    if not path.exists(configuration_file_path):
        logging.fatal(
            f"Cannot find the configuration file {configuration_file_path}.")
        quit()

    with open(configuration_file_path, "r") as f:
        configuration = json.load(f)["Configuration"]

    input = path.abspath(configuration["test_case_to_execute_folder"])
    if not path.isdir(input):
        logging.fatal(f"Cannot find the test case folder {input}.")
        quit()
    else:
        logging.debug(f"Executing test cases from {input}.")

    output = path.abspath(configuration["test_case_executed_folder"])
    logging.debug(f"Storing results in {output}.")

    faban_master = f"http://{configuration['faban_ip']}:9980/"
    faban_client = path.abspath(
        "./faban/benchflow-faban-client/target/benchflow-faban-client.jar")

    command_to_execute_before_a_test = configuration["pre_exec_external_command"]
    command_to_execute_after_a_test = configuration["post_exec_external_command"]
    command_to_execute_at_a_test = configuration["on_exec_external_command"]
    seconds_to_wait_for_deployment = int(
        configuration["test_case_waiting_for_deployment_in_seconds"])

    time_to_complete_one_test = int(configuration["test_case_ramp_up_in_seconds"]) + int(
        configuration["test_case_ramp_up_in_seconds"]) + int(configuration["test_case_ramp_up_in_seconds"])

    for f in os.scandir(input):
        if (path.isdir(f)):
            try:
                logging.info(f"Executing test case {f.name}.")

                if (len(command_to_execute_before_a_test) > 0):
                    run_external_applicaton(
                        command_to_execute_before_a_test, "Running external application before the test.")

                test_id = f.name
                command_deploy_stack = f"docker stack deploy --compose-file={f.path}/docker-compose.yml {test_id}"

                run_external_applicaton(
                    command_deploy_stack, "Deploying the system under test.")

                wait(seconds_to_wait_for_deployment, "Waiting for deployment")

                driver = f"{input}/{test_id}/{test_id}.jar"
                driver_configuration = f"{input}/{test_id}/run.xml"
                deployment_descriptor = f"{input}/{test_id}/docker-compose.yml"
                temporary_file = f"{test_id}_run_id.tmp"
                command_deploy_faban = f"java -jar {faban_client} {faban_master} deploy {test_id} {driver} {driver_configuration} > {temporary_file}"

                run_external_applicaton(
                    command_deploy_faban, "Deploying the load driver.")

                with open(temporary_file, "r") as f:
                    std_out_deploy_faban = f.readline().rstrip()
                run_id = std_out_deploy_faban
                logging.debug(f"Obtained {run_id} as run ID.")
                os.remove(temporary_file)

                logging.info("Waiting for the test to be completed")
                status = ""
                external_tool_was_started = False

                time_elapsed = 0
                while ((status != "COMPLETED") and (status != "FAILED")):
                    command_status_faban = f"java -jar {faban_client} {faban_master} status {run_id} > {temporary_file}"

                    run_external_applicaton(
                        command_status_faban, "Getting the status from Faban.")

                    with open(temporary_file, "r") as f:
                        std_out_status_faban = f.readline().rstrip()
                    status = std_out_status_faban
                    logging.debug(f"Obtained {status} as status.")
                    os.remove(temporary_file)

                    if (status == "STARTED" and external_tool_was_started == False and len(command_to_execute_before_a_test) > 0):
                        external_tool_was_started = True
                        run_external_applicaton(
                            command_to_execute_at_a_test, "Running external application with the test.")

                    if ((status != "COMPLETED") and (status != "FAILED")):
                        wait(60, "Waiting for Faban to complete")
                        time_elapsed = time_elapsed + 60

                if (len(command_to_execute_after_a_test) > 0):
                    run_external_applicaton(
                        command_to_execute_after_a_test, "Running external application after the test.")
            finally:
                command_undeploy_stack = f"docker stack rm {test_id}"
                run_external_applicaton(
                    command_undeploy_stack, "Undeploying the system under test.", False)

                if path.isfile(temporary_file):
                    os.remove(temporary_file)

            if (status == "COMPLETED"):
                logging.info("Saving test results")
                test_output_path = f"{output}/{test_id}/faban"
                os.makedirs(test_output_path)

                command_info_faban = f"java -jar {faban_client} {faban_master} info {run_id} > {f.name}_status.tmp"
                shutil.copyfile(path.abspath(
                    f"./faban/output/{run_id}/summary.xml"), test_output_path)
                shutil.copyfile(path.abspath(
                    f"./faban/output/{run_id}/detail.xan"), test_output_path)
                shutil.copyfile(path.abspath(
                    f"./faban/output/{run_id}/log.xml"), test_output_path)
                shutil.move(f.path, f"{output}/{test_id}/definition")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("--configuration", metavar="path_to_configuration_file",
                        help="Configuration file", default="configuration.json")
    parser.add_argument("--logging", help="Logging level",
                        type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    execute_test(args.configuration)
