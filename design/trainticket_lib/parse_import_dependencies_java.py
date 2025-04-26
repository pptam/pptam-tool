#!/usr/bin/env python3

import os
import re
import json
import argparse
import logging
import subprocess

def extract_service_dependencies(root_dir, subfolders):
    pattern = re.compile(r'http://(ts-[a-zA-Z0-9\-]+-service)')
    service_names = {}

    for subfolder in subfolders:
        full_path = os.path.abspath(os.path.join(root_dir, subfolder))
        logging.info(f"Analyzing folder {full_path}...")
        for dirpath, _, filenames in os.walk(full_path):
            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.readlines()
                            for line in content:
                                if line.lstrip().startswith("//"):
                                    continue
                                matches = pattern.findall(line)
                                if matches:
                                    if subfolder not in service_names:
                                        service_names[subfolder] = []
                                    service_names[subfolder].extend(matches)
                    except Exception as e:
                        logging.error(f"Failed to process file {file_path}: {e}")

    return service_names

def find_selected_jars(root_folder, selected_subfolders):
    jar_paths = {}
    for folder_name in selected_subfolders:
        service_path = os.path.join(root_folder, folder_name)
        target_path = os.path.abspath(os.path.join(service_path, 'target'))
        if os.path.isdir(target_path):
            for file_name in os.listdir(target_path):
                if file_name.endswith('.jar'):
                    jar_path = os.path.join(target_path, file_name)
                    logging.info(f"Including jar {jar_path}...")
                    jar_paths[folder_name] = jar_path
    return jar_paths

def analyze_jar(jar_path, all_jars_classpath):
    try:
        result = subprocess.run(
            ['jdeps', '-cp', all_jars_classpath, '-verbose', jar_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except Exception as e:
        logging.error(f"Failed to analyze jar {jar_path}: {e}")
        return ""

def extract_dependencies(jdeps_output, target_package):
    dependencies = []
    for line in jdeps_output.splitlines():
        if '->' in line:
            parts = line.split('->')
            if len(parts) == 2:
                source = parts[0].strip()
                dependency_part = parts[1].strip()
                dependency = dependency_part.split()[0]
                if dependency.startswith(target_package):
                    source_clean = source.split('$')[0]
                    dependencies.append((source_clean, dependency))
    return dependencies

def run_analysis(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    subfolders_to_traverse = config["subfolders_to_traverse"]
    target_package = config["target_package"]
    root_folder = config["root_folder"]

    all_jars_dict = find_selected_jars(root_folder, subfolders_to_traverse)
    all_jars_classpath = ':'.join(all_jars_dict.values())

    results = [] # contains ['microservice', 'source', 'dependency']
    for service_name, jar_path in all_jars_dict.items():
        analysis = analyze_jar(jar_path, all_jars_classpath)
        dependencies = extract_dependencies(analysis, target_package)
        for source_class, dependency_class in dependencies:
            results.append([service_name, source_class, dependency_class])

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze import dependencies from JAR files.")
    parser.add_argument("config_file", help="Path to the configuration JSON file.")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    for line in run_analysis(args.config_file):
        print(";".join(line))