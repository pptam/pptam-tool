#!/usr/bin/env python3

import analyze_import_dependencies

def run_analysis():
    return analyze_import_dependencies.run_analysis("./analyze_import_dependencies.json")

if __name__ == "__main__":
    for line in run_analysis():
        print(";".join(line))
