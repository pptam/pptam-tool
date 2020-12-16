#!/usr/bin/env python3

import os
import time
import argparse
import logging
import shutil
import configparser
import datetime
import csv
from pluginbase import PluginBase
from lib import run_external_applicaton, replace_values_in_file

def run_plugins(configuration, section, func):
    plugins = configuration[section]["enabled_plugins"].split()
    
    plugin_base = PluginBase(package='plugins')
    plugin_source = plugin_base.make_plugin_source(searchpath=['./plugins'])
    for plugin_name in plugin_source.list_plugins():
        if not plugin_name.startswith("_") and (any("all" in p for p in plugins) or any(plugin_name in p for p in plugins)):
            plugin = plugin_source.load_plugin(plugin_name)
            try:
                function_to_call = getattr(plugin, func, None)
                if function_to_call!=None:
                    function_to_call()
            except:
                logging.critical(f"Cannot invoke plugin {plugin_name}.")
    
def perform_test(configuration, section, repetition, overwrite_existing_results):
    run_plugins(configuration, section, "setup")

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

    driver = f"{output}/locustfile.py"
    deployment_descriptor = f"{output}/docker-compose.yml"

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

    seconds_to_wait_for_deployment = int(configuration[section]["test_case_waiting_for_deployment_in_seconds"])
    seconds_to_wait_for_undeployment = int(configuration[section]["test_case_waiting_for_undeployment_in_seconds"])

    try:
        if os.path.exists(deployment_descriptor):
            command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} {test_id}"
            run_external_applicaton(command_deploy_stack)
            logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
            time.sleep(seconds_to_wait_for_deployment)

        run_plugins(configuration, section, "before")

        host = configuration[section]["locust_host_url"]
        load = configuration[section]["load"]
        spawn_rate = configuration[section]["spawn_rate_per_second"]
        run_time = configuration[section]["run_time_in_seconds"]
        log_file = os.path.splitext(driver)[0] + ".log"
        out_file = os.path.splitext(driver)[0] + ".out"
        csv_prefix = os.path.join(os.path.dirname(driver), "result")
        logging.info(f"Running the load test for {test_id}, with {load} users, running for {run_time} seconds.")
        run_external_applicaton(
            f'locust --locustfile {driver} --host {host} --users {load} --spawn-rate {spawn_rate} --run-time {run_time}s --headless --only-summary --csv {csv_prefix} --csv-full-history --logfile "{log_file}" --loglevel DEBUG >> {out_file} 2> {out_file}', False)

        run_plugins(configuration, section, "after")
    finally:
        if os.path.exists(deployment_descriptor):
            command_undeploy_stack = f"docker stack rm {test_id}"
            run_external_applicaton(command_undeploy_stack, False)
            logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
            time.sleep(seconds_to_wait_for_undeployment)

    run_plugins(configuration, section, "teardown")
    logging.info(f"Test {test_id} completed. Test results can be found in {output}.")

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
