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
import jinja2

plugin_source = None

def run_plugins(configuration, section, design_path, output, test_id, func):
    result = []
    plugin_list = configuration[section]["enabled_plugins"].split()    
    global plugin_source
    
    if plugin_source==None:
        plugin_base = PluginBase(package='plugins')
        plugin_source = plugin_base.make_plugin_source(searchpath=['./plugins'])

    for plugin_name in plugin_list:        
        logging.debug(f"Executing {func} of plugin {plugin_name}.")
        
        plugin = plugin_source.load_plugin(plugin_name)
        try:
            function_to_call = getattr(plugin, func, None)
            if function_to_call!=None:
                call_result = function_to_call(configuration[section], design_path, output, test_id)
                result.append(call_result)
                
        except Exception as e:
            logging.critical(f"Cannot invoke plugin {plugin_name}: {repr(e)}")
    
    return result

def create_output_directory(configuration, section, commit):
    now = datetime.datetime.now()
    test_id_without_timestamp = configuration[section]["test_case_prefix"].lower() + "-" + section.lower()
    if commit is not None:
        test_id_without_timestamp = test_id_without_timestamp + "-" + commit[:8]
    test_id = now.strftime("%Y%m%d%H%M") + "-" + test_id_without_timestamp

    all_outputs = os.path.abspath(os.path.join("./executed"))
    if not os.path.isdir(all_outputs):
        logging.debug(f"Creating {all_outputs}, since it does not exist.")
        os.makedirs(all_outputs)
    
    if any(x.endswith(test_id_without_timestamp) for x in os.listdir(all_outputs)):
        name_of_existing_folder = next(x for x in os.listdir(all_outputs) if x.endswith(test_id_without_timestamp))
        logging.warning(f"Skipping {name_of_existing_folder}, since it already exists.")
        return None, None, None

    output = os.path.join(all_outputs, test_id)
    os.makedirs(output)

    return output, test_id, now

def perform_test(configuration, section, design_path, project, commit):
    output, test_id, now = create_output_directory(configuration, section, commit)
    if output==None:
        return
        
    logging.debug(f"Created a folder name {test_id} in {output}.")

    plugin_files = run_plugins(configuration, section, design_path, output, test_id, "get_configuration_files")
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
        f.write(f"TIMESTAMP={now.timestamp()}\n")
        f.write(f"TEST_NAME={test_id}\n")
        f.write(f"GIT_PROJECT={project}\n")
        f.write(f"GIT_COMMIT={commit}\n")


    logging.info(f"Executing test case {test_id}.")

    enable_phase_setup = configuration[section]["enable_phase_setup"].strip()=="1"
    enable_phase_deploy = configuration[section]["enable_phase_deploy"].strip()=="1"
    enable_phase_before = configuration[section]["enable_phase_before"].strip()=="1"
    enable_phase_run = configuration[section]["enable_phase_run"].strip()=="1"
    enable_phase_after = configuration[section]["enable_phase_after"].strip()=="1"
    enable_phase_undeploy = configuration[section]["enable_phase_undeploy"].strip()=="1"
    enable_phase_teardown = configuration[section]["enable_phase_teardown"].strip()=="1"

    seconds_to_wait_before_setup = int(configuration[section]["seconds_to_wait_before_setup"])
    seconds_to_wait_before_deploy = int(configuration[section]["seconds_to_wait_before_deploy"])
    seconds_to_wait_before_before = int(configuration[section]["seconds_to_wait_before_before"])
    seconds_to_wait_before_run = int(configuration[section]["seconds_to_wait_before_run"])
    seconds_to_wait_before_after = int(configuration[section]["seconds_to_wait_before_after"])
    seconds_to_wait_before_undeploy = int(configuration[section]["seconds_to_wait_before_undeploy"])
    seconds_to_wait_before_teardown = int(configuration[section]["seconds_to_wait_before_teardown"])

    if enable_phase_setup:
        logging.debug(f"Waiting for {seconds_to_wait_before_setup} seconds.")
        time.sleep(seconds_to_wait_before_setup)
        run_plugins(configuration, section, design_path, output, test_id, "setup")
    
    if enable_phase_deploy:
        logging.debug(f"Waiting for {seconds_to_wait_before_deploy} seconds.")
        time.sleep(seconds_to_wait_before_deploy)
        run_plugins(configuration, section, design_path, output, test_id, "deploy")

    plugins_are_ready = None
    for _ in range(10):   
        plugins_are_ready = run_plugins(configuration, section, design_path, output, test_id, "ready")

        if not (False in plugins_are_ready):
            break

        logging.critical("Cannot start because not all plugins are ready, waiting 1 min.")
        time.sleep(60)

    if (plugins_are_ready is None) or (False in plugins_are_ready):
        logging.critical("Cannot start because not all plugins are ready.")
    else:
        if enable_phase_before:
            logging.debug(f"Waiting for {seconds_to_wait_before_before} seconds.")
            time.sleep(seconds_to_wait_before_before)
            run_plugins(configuration, section, design_path, output, test_id, "before")

        if enable_phase_run:
            logging.debug(f"Waiting for {seconds_to_wait_before_run} seconds.")
            time.sleep(seconds_to_wait_before_run)
            run_plugins(configuration, section, design_path, output, test_id, "run")

        if enable_phase_after:
            logging.debug(f"Waiting for {seconds_to_wait_before_after} seconds.")
            time.sleep(seconds_to_wait_before_after)
            run_plugins(configuration, section, design_path, output, test_id, "after")

    if enable_phase_undeploy:
        logging.debug(f"Waiting for {seconds_to_wait_before_undeploy} seconds.")
        time.sleep(seconds_to_wait_before_undeploy)
        run_plugins(configuration, section, design_path, output, test_id, "undeploy")

    if enable_phase_teardown:
        logging.debug(f"Waiting for {seconds_to_wait_before_teardown} seconds.")
        time.sleep(seconds_to_wait_before_teardown)
        run_plugins(configuration, section, design_path, output, test_id, "teardown")

    logging.info(f"Test {test_id} completed. Test results can be found in {output}.")

def execute_tests(design_path,project,commit):
    if os.path.exists(os.path.join(design_path, "test_plan.ini.jinja")):
        template_loader = jinja2.FileSystemLoader(searchpath=design_path)
        template_environment = jinja2.Environment(loader=template_loader)
        template_file = "test_plan.ini.jinja"
        template = template_environment.get_template(template_file)
        outputText = template.render()
        with open(os.path.join(design_path, "test_plan.ini"), "w") as f:
            f.write(outputText)

    configuration = configparser.ConfigParser()
    configuration.read([os.path.join(design_path, "configuration.ini"), os.path.join(design_path, "test_plan.ini")])
    
    run_plugins(configuration, "DEFAULT", design_path, None, None, "setup_all")

    for section in configuration.sections():
        if section.lower().startswith("test"):
            enabled = (configuration[section]["enabled"] == "1")
            if enabled:
                perform_test(configuration, section, design_path,project,commit)

    run_plugins(configuration, "DEFAULT", design_path, None, None, "teardown_all")

    logging.info(f"Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("design", metavar="path_to_design_folder", help="Design folder")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    parser.add_argument("--projectname", help="Name of the project", type=str, default="")
    parser.add_argument("--commit", help="Link execution to specific commit identifier", type=str, default="")
    # 1 Agg argument con dati git e poi si passa per cartella e commit ecc.
    # 2 design_folder deve esistere e essere copiata di qua
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    logging.getLogger("requests").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)

        
    if args.design is None or args.design == "" or (not os.path.exists(args.design)):
        logging.fatal(f"Cannot find the design folder {args.design}. Please indicate one.")
        quit()

    execute_tests(args.design, args.projectname, args.commit)  
        
