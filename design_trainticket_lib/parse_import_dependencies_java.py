#!/usr/bin/env python3

import os
import subprocess
import csv
import json

def find_selected_jars(root_folder, selected_subfolders):
    jar_paths = {}
    for folder_name in selected_subfolders:
        service_path = os.path.join(root_folder, folder_name)
        target_path = os.path.join(service_path, 'target')
        if os.path.isdir(target_path):
            for file_name in os.listdir(target_path):
                if file_name.endswith('.jar'):
                    jar_path = os.path.join(target_path, file_name)
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
    except Exception:
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
    solution_folder = config["solution_folder"]

    all_jars_dict = find_selected_jars(solution_folder, subfolders_to_traverse)
    all_jars_classpath = ':'.join(all_jars_dict.values())

    results = [] # contains ['microservice', 'source', 'dependency']
    for service_name, jar_path in all_jars_dict.items():
        analysis = analyze_jar(jar_path, all_jars_classpath)
        dependencies = extract_dependencies(analysis, target_package)
        for source_class, dependency_class in dependencies:
            results.append([service_name, source_class, dependency_class])

    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python analyze_import_dependencies.py <config_file.json>")
        sys.exit(1)
    for line in run_analysis(sys.argv[1]):
        print(";".join(line))
