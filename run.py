#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="Test case generation and execution.")
parser.add_argument("--configuration", help="The configuration file to read.", default="configuration.json")
args = parser.parse_args()

# testExecutorDestination = rootDirectory+"/run"
# parseConfiguration = parser.getParseConfiguration()
# testExecutor = TestExecutor(rootDirectory, parseConfiguration)
# testExecutor.executeTests(testExecutorDestination)
