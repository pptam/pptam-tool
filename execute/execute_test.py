#!/usr/bin/env python3

import os
import time
import argparse
import logging
import shutil
import configparser
import datetime
import csv
import json
from pluginbase import PluginBase
from lib import run_external_applicaton, replace_values_in_file

global_plugin_state = {}

def run_plugins(configuration, section, output, test_id, func):
    result = []
    plugins = configuration[section]["enabled_plugins"].split()
    
    plugin_base = PluginBase(package='plugins')
    plugin_source = plugin_base.make_plugin_source(searchpath=['./plugins'])
    plugin_list = sorted(plugin_source.list_plugins())

    for plugin_name in plugin_list:
        if not plugin_name.startswith("_") and (("all" in plugins) or (plugin_name in plugins)):
            if f"!{plugin_name}" in plugins:
                logging.debug(f"Skipping plugin {plugin_name}.")
            else:
                logging.debug(f"Executing {func} of plugin {plugin_name}.")
                plugin = plugin_source.load_plugin(plugin_name)
                try:
                    function_to_call = getattr(plugin, func, None)
                    if function_to_call!=None:
                        plugin_state = ", ".join(global_plugin_state.keys())
                        logging.info(f"Current plugin state contains [{plugin_state}]")

                        call_result = function_to_call(global_plugin_state, configuration[section], output, test_id)
                        result.append(call_result)
                        
                except Exception as e:
                    logging.critical(f"Cannot invoke plugin {plugin_name}: {e}")
    
    return result

def create_output_directory(configuration, section, overwrite_existing_results):
    now = datetime.datetime.now()
    test_id_without_timestamp = configuration[section]["test_case_prefix"].lower() + "-" + section.lower()
    test_id = now.strftime("%Y%m%d%H%M") + "-" + test_id_without_timestamp

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
            return None, None

    output = os.path.join(all_outputs, test_id)
    os.makedirs(output)

    return output, test_id

def perform_test(configuration, section, overwrite_existing_results):
    output, test_id = create_output_directory(configuration, section, overwrite_existing_results)
    if output==None:
        return
        
    logging.debug(f"Created a folder name {test_id} in {output}.")

    plugin_files = run_plugins(configuration, section, output, test_id, "get_configuration_files")
    plugin_files = [item for sublist in plugin_files for item in sublist]
    for plugin_file in plugin_files:
        if os.path.exists(os.path.join(design_path, plugin_file)):
            shutil.copyfile(os.path.join(design_path, plugin_file), os.path.join(output, plugin_file))

    replacements = []
    for entry in configuration[section].keys():
        replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configuration[section][entry]})
        replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": configuration[section][entry]})

    replacements.append({"search_for": "${TEST_NAME}", "replace_with": test_id})

    logging.debug(f"Replacing values.")
    for plugin_file in plugin_files:
        if os.path.join(output, plugin_file):
            replace_values_in_file(os.path.join(output, plugin_file), replacements)

    with open(os.path.join(output, "configuration.ini"), "w") as f:
        f.write(f"[CONFIGURATION]\n")
        for option in configuration.options(section):
            f.write(f"{option.upper()}={configuration[section][option]}\n")

    logging.info(f"Executing test case {test_id}.")

    seconds_to_wait_before_setup = int(configuration[section]["seconds_to_wait_before_setup"])
    seconds_to_wait_before_deploy = int(configuration[section]["seconds_to_wait_before_deploy"])
    seconds_to_wait_before_before = int(configuration[section]["seconds_to_wait_before_before"])
    seconds_to_wait_before_run = int(configuration[section]["seconds_to_wait_before_run"])
    seconds_to_wait_before_after = int(configuration[section]["seconds_to_wait_before_after"])
    seconds_to_wait_before_undeploy = int(configuration[section]["seconds_to_wait_before_undeploy"])
    seconds_to_wait_before_teardown = int(configuration[section]["seconds_to_wait_before_teardown"])

    logging.debug(f"Waiting for {seconds_to_wait_before_setup} seconds.")
    time.sleep(seconds_to_wait_before_setup)
    run_plugins(configuration, section, output, test_id, "setup")
    
    logging.debug(f"Waiting for {seconds_to_wait_before_deploy} seconds.")
    time.sleep(seconds_to_wait_before_deploy)
    run_plugins(configuration, section, output, test_id, "deploy")

    plugins_are_ready = None
    for _ in range(10):   
        plugins_are_ready = run_plugins(configuration, section, output, test_id, "ready")

        if not (False in plugins_are_ready):
            break

        logging.critical("Cannot start because not all plugins are ready, waiting 1 min.")
        time.sleep(60)

    if (plugins_are_ready is None) or (False in plugins_are_ready):
        logging.critical("Cannot start because not all plugins are ready.")
    else:
        logging.debug(f"Waiting for {seconds_to_wait_before_before} seconds.")
        time.sleep(seconds_to_wait_before_before)
        run_plugins(configuration, section, output, test_id, "before")

        logging.debug(f"Waiting for {seconds_to_wait_before_run} seconds.")
        time.sleep(seconds_to_wait_before_run)
        run_plugins(configuration, section, output, test_id, "run")

        logging.debug(f"Waiting for {seconds_to_wait_before_after} seconds.")
        time.sleep(seconds_to_wait_before_after)
        run_plugins(configuration, section, output, test_id, "after")

    logging.debug(f"Waiting for {seconds_to_wait_before_undeploy} seconds.")
    time.sleep(seconds_to_wait_before_undeploy)
    run_plugins(configuration, section, output, test_id, "undeploy")

    logging.debug(f"Waiting for {seconds_to_wait_before_teardown} seconds.")
    time.sleep(seconds_to_wait_before_teardown)
    run_plugins(configuration, section, output, test_id, "teardown")

    logging.info(f"Test {test_id} completed. Test results can be found in {output}.")

def execute_test(design_path, overwrite_existing_results):
    configuration = configparser.ConfigParser()
    configuration.read([os.path.join(design_path, "configuration.ini"), os.path.join(design_path, "test_plan.ini")])

    run_plugins(configuration, "DEFAULT", design_path, None, "setup_all")

    for section in configuration.sections():
        if section.lower().startswith("test"):
            enabled = (configuration[section]["enabled"] == "1")
            if enabled:
                perform_test(configuration, section, overwrite_existing_results)

    run_plugins(configuration, "DEFAULT", design_path, None, "teardown_all")

    logging.info(f"Done.")

if __name__ == "__main__":
    overwrite_data = False
    design_path = None
    logging_level = 2

    if os.path.exists("./arguments.ini"):
        arguments = configparser.ConfigParser()
        arguments.read("./arguments.ini")
        overwrite_data = arguments["ARGUMENTS"]["OVERWRITE"] == "1"
        design_path = arguments["ARGUMENTS"]["DESIGN"]
        logging_level = int(arguments["ARGUMENTS"]["LOGGING"])
    else:
        parser = argparse.ArgumentParser(description="Executes test cases.")
        parser.add_argument("--design", metavar="path_to_design_folder", help="Design folder")
        parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=2)
        parser.add_argument("--overwrite", help="Overwrite existing test cases", action='store_true', default=False)

        args = parser.parse_args()

        overwrite_data = args.overwrite
        design_path = args.design
        logging_level = args.logging

    logging.basicConfig(format='%(message)s', level=logging_level * 10)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
        
    if design_path is None or design_path == "" or (not os.path.exists(design_path)):
        logging.fatal(f"Cannot find the design folder. Please indicate one with the parameter --design")
        quit()

    execute_test(design_path, overwrite_data)
