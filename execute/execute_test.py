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
    for plugin_name in plugin_source.list_plugins():
        if not plugin_name.startswith("_") and (any("all" in p for p in plugins) or any(plugin_name in p for p in plugins)):
            logging.debug(f"Executing {func} of plugin {plugin_name}.")
            plugin = plugin_source.load_plugin(plugin_name)
            try:
                function_to_call = getattr(plugin, func, None)
                if function_to_call!=None:
                    logging.info(f"Current plugin state contains {global_plugin_state.keys()}")

                    call_result = function_to_call(global_plugin_state, configuration[section], output, test_id)
                    result.append(call_result)
                    
            except Exception as e:
                logging.critical(f"Cannot invoke plugin {plugin_name}: {e}")
    
    return result

def create_output_directory(configuration, section, repetition, overwrite_existing_results):
    now = datetime.datetime.now()
    test_id_without_timestamp = configuration[section]["test_case_prefix"].lower() + "-" + section.lower() + "-" + str(repetition + 1)
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

def perform_test(configuration, section, repetition, overwrite_existing_results):
    output, test_id = create_output_directory(configuration, section, repetition, overwrite_existing_results)
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

    run_plugins(configuration, section, output, test_id, "setup")
    run_plugins(configuration, section, output, test_id, "deploy")
        
    plugins_are_ready = run_plugins(configuration, section, output, test_id, "ready")
    if False in plugins_are_ready:
        logging.critical("Cannot start because not all plugins are ready.")
    else:
        run_plugins(configuration, section, output, test_id, "before")
        run_plugins(configuration, section, output, test_id, "run")
        run_plugins(configuration, section, output, test_id, "after")

    run_plugins(configuration, section, output, test_id, "undeploy")
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
                repeat = int(configuration[section]["repeat"])
                for repetition in range(repeat):
                    perform_test(configuration, section, repetition, overwrite_existing_results)

    run_plugins(configuration, "DEFAULT", design_path, None, "teardown_all")

    logging.info(f"Done.")

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.client.mount('https://', HTTPAdapter(pool_maxsize=100))
    self.client.mount('http://', HTTPAdapter(pool_maxsize=100))

if __name__ == "__main__":
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("--design", metavar="path_to_design_folder", help="Design folder")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=2)
    parser.add_argument("--overwrite", help="Overwrite existing test cases", action='store_true', default=False)

    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    design_path = args.design
    if design_path == None or (not os.path.exists(design_path)):
        logging.fatal(f"Cannot find the design folder. Please indicate one with the parameter --design")
        quit()

    execute_test(design_path, args.overwrite)
