#!/usr/bin/env python

import os
import time
import argparse
import logging
from os import path
import json
from time import sleep
import subprocess
import shutil
import configparser
import uuid
from datetime import datetime
from lib import progress, run_external_applicaton, wait, replace_values_in_file


def add_faban_job(configuration, section, repetition):
    output = path.abspath(path.join("./", configuration["DEFAULT"]["test_case_creation_folder"]))
    if not path.isdir(output):
        logging.debug(f"Creating {output}, since it does not exist.")
        os.makedirs(output)

    path_to_benchmark = path.abspath("./benchmark")
    path_to_drivers = path.abspath("./drivers")
    path_to_temp = path.join(path_to_drivers, "tmp")

    now = datetime.now()
    test_id = configuration[section]["test_case_prefix"].lower() + "-" + \
        now.strftime("%Y%m%d%H%M%S") + "-" + section.lower() + "-" + str(repetition+1)
    logging.debug(f"Generating a test with the id {test_id} in {path_to_temp}.")

    if path.isdir(path_to_temp):
        shutil.rmtree(path_to_temp)

    logging.debug(f"Creating new job, based on the templates in {path_to_benchmark}.")
    shutil.copytree(path_to_benchmark, path_to_temp)
    shutil.copyfile(path.join(design_path, configuration[section]["deployment_descriptor"]), path.join(path_to_temp, "deploy", "docker-compose.yml"))
    shutil.copyfile(path.join(design_path, configuration[section]["faban_driver"]), path.join(path_to_temp, "src", "pptam", "driver", "WebDriver.java"))
    shutil.copyfile(path.join(design_path, configuration[section]["faban_benchmark"]), path.join(path_to_temp, "src", "pptam", "harness", "WebBenchmark.java"))

    replacements = []
    for entry in configuration[section].keys():
        replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configuration[section][entry]})
        replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": configuration[section][entry]})

    replacements.append({"search_for": "${TEST_NAME}", "replace_with": test_id})

    logging.debug(f"Replacing values.")
    replace_values_in_file(path.join(path_to_temp, "build.properties"), replacements)
    replace_values_in_file(path.join(path_to_temp, "deploy", "run.xml"), replacements)
    shutil.copyfile(path.join(path_to_temp, "deploy", "run.xml"), path.join(path_to_temp, "config", "run.xml"))
    replace_values_in_file(path.join(path_to_temp, "src", "pptam", "driver", "WebDriver.java"), replacements)
    replace_values_in_file(path.join(path_to_temp, "src", "pptam", "harness", "WebBenchmark.java"), replacements)
    replace_values_in_file(path.join(path_to_temp, "deploy", "docker-compose.yml"), replacements)

    logging.debug("Compiling the Faban benchmark")
    current_folder = os.getcwd()
    os.chdir(path_to_temp)
    command = "ant deploy.jar -q -S"
    result = os.system(command)
    os.chdir(current_folder)

    if result != 0:
        logging.fatal(f"Could not compile job in {path_to_temp}.")
        quit()

    path_to_output = path.join(path.abspath(output), test_id)
    logging.info(f"Writing the job into {path_to_output}.")

    os.makedirs(path_to_output)
    shutil.copyfile(path.join(path_to_temp, "build", f"{test_id}.jar"), path.join(path_to_output, f"{test_id}.jar"))
    shutil.copyfile(path.join(path_to_temp, "config", "run.xml"), path.join(path_to_output, "run.xml"))
    shutil.copyfile(path.join(path_to_temp, "deploy", "docker-compose.yml"), path.join(path_to_output, "docker-compose.yml"))

    with open(path.join(path_to_output, "configuration.txt"), "w") as f:
        for option in configuration.options(section):
            f.write(f"{option}={configuration[section][option]}\n")

    shutil.move(path_to_temp, path.join(path_to_drivers, test_id))


def prepare_execution(design_path):
    configuration = configparser.ConfigParser()
    configuration.read([path.join(design_path, "test_case.ini"), path.join(design_path, "test_plan.ini")])

    for section in configuration.sections():
        if section.lower().startswith("test"):
            enabled = (configuration[section]["enabled"] == "1")
            if enabled:
                repeat = int(configuration[section]["repeat"])
                for repetition in range(repeat):
                    add_faban_job(configuration, section, repetition)

    logging.info(f"Done.")


def execute_test(design_path):
    configuration = configparser.ConfigParser()
    configuration.read(path.join(design_path, "test_case.ini"))

    input = path.abspath(path.join("./", configuration["DEFAULT"]["test_case_creation_folder"]))
    if not path.isdir(input):
        logging.fatal(f"Cannot find the test case folder {input}.")
        raise RuntimeError
    else:
        logging.debug(f"Executing test cases from {input}.")

    seconds_to_wait_for_deployment = int(configuration["DEFAULT"]["test_case_waiting_for_deployment_in_seconds"])
    seconds_to_wait_for_undeployment = int(configuration["DEFAULT"]["test_case_waiting_for_undeployment_in_seconds"])
    time_to_complete_one_test = seconds_to_wait_for_deployment + seconds_to_wait_for_undeployment + (((int(configuration["test_case_ramp_up_in_seconds"]) + int(configuration["test_case_steady_state_in_seconds"]) + int(configuration["test_case_ramp_down_in_seconds"])) // 60) + 1) * 60
    time_to_complete_all_tests = (len([name for name in os.listdir(f"{input}/") if os.path.isdir(f"{input}/{name}")]) * time_to_complete_one_test // 60) + 1
    logging.info(f"Estimated duration of ONE test: approx. {time_to_complete_one_test} seconds.")
    logging.info(f"Estimated duration of ALL tests: approx. {time_to_complete_all_tests} minutes.")

    output = path.abspath(path.join("./", configuration["DEFAULT"]["test_case_executed_folder"]))
    logging.debug(f"Storing results in {output}.")

    faban_master = f"http://{configuration['DEFAULT']['faban_ip']}:9980/"
    faban_client = path.abspath("./faban/benchflow-faban-client/target/benchflow-faban-client.jar")

    command_to_execute_before_a_test = configuration["DEFAULT"]["pre_exec_external_command"]
    command_to_execute_after_a_test = configuration["DEFAULT"]["post_exec_external_command"]
    command_to_execute_at_a_test = configuration["DEFAULT"]["on_exec_external_command"]
    sut_ip = configuration["DEFAULT"]["sut_ip"]
    sut_port = configuration["DEFAULT"]["sut_port"]

    for f in os.scandir(input):
        if (path.isdir(f)):
            try:
                logging.info(f"Executing test case {f.name}.")

                if (len(command_to_execute_before_a_test) > 0):
                    run_external_applicaton(f"{command_to_execute_before_a_test} {sut_ip} {sut_port}")

                test_id = f.name
                temporary_file = f"{test_id}.tmp"

                test_output_path = f"{output}/{test_id}"
                if path.isdir(test_output_path):
                    logging.info(f"Removing path {test_output_path} since it already exists.")
                    shutil.rmtree(path, ignore_errors=False, onerror=RuntimeError)

                deployment_descriptor = f"{input}/{test_id}/docker-compose.yml"
                command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} {test_id}"

                run_external_applicaton(command_deploy_stack)

                logging.debug(f"Waiting for {seconds_to_wait_for_deployment} seconds.")
                wait(seconds_to_wait_for_deployment, time_to_complete_one_test, "Waiting for deployment.", 0)
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
                        run_external_applicaton(f"{command_to_execute_at_a_test} {sut_ip} {sut_port}")

                    if ((status != "COMPLETED") and (status != "FAILED")):
                        if time_elapsed < time_to_complete_one_test:
                            wait_until = 60
                        else:
                            wait_until = 10

                        logging.debug(f"Waiting for {wait_until} seconds.")
                        wait(wait_until, time_to_complete_one_test, "Waiting for test to finish.", time_elapsed, time_to_complete_one_test - seconds_to_wait_for_undeployment)
                        time_elapsed += wait_until

                if (len(command_to_execute_after_a_test) > 0):
                    run_external_applicaton(f"{command_to_execute_after_a_test} {sut_ip} {sut_port}")
            finally:
                command_undeploy_stack = f"docker stack rm {test_id}"
                run_external_applicaton(command_undeploy_stack, False)

                if path.isfile(temporary_file):
                    os.remove(temporary_file)

            if (status == "COMPLETED"):
                logging.debug(f"Waiting for {seconds_to_wait_for_undeployment} seconds.")
                wait(seconds_to_wait_for_undeployment, time_to_complete_one_test, "Waiting for undeployment.  ", time_elapsed)
                progress(time_to_complete_one_test, time_to_complete_one_test, "Done.                      \n")

                os.makedirs(test_output_path)
                shutil.copytree(f"./faban/output/{run_id}", f"{test_output_path}/faban")
                shutil.move(f"{input}/{test_id}", f"{test_output_path}/definition")

                command_info_faban = f"java -jar {faban_client} {faban_master} info {run_id} > {test_output_path}/faban/runInfo.txt"
                run_external_applicaton(command_info_faban)

                logging.info(f"Test {test_id} completed. Test results can be found in {test_output_path}.")
            else:
                progress(time_to_complete_one_test, time_to_complete_one_test, "Failed.                    \n")
                logging.fatal(f"Test {test_id} with run id {run_id} failed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("--design", metavar="path_to_design_folder", help="Design folder", default="../design")
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)
    parser.add_argument("--cleanup", help="Deletes all temporary data", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)

    design_path = args.design
    if not path.exists(design_path):
        logging.fatal(f"Cannot find the design folder {design_path}.")
        quit()

    configuration = configparser.ConfigParser()
    configuration.read(path.join(design_path, "test_case.ini"))

    if args.cleanup:
        output = path.abspath(path.join("./", configuration["DEFAULT"]["test_case_creation_folder"]))
        if path.isdir(output):
            shutil.rmtree(output)

    output = path.abspath(path.join("./", configuration["DEFAULT"]["test_case_creation_folder"]))
    if path.isdir(output) and len(os.listdir(output)) > 0:
        logging.info(f"Found exiting jobs in {output}, continue execution.")
    else:
        logging.info(f"Generating jobs.")
        prepare_execution(design_path)
