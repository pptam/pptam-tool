#!/usr/bin/env python
import sys
import logging
import os
import time
import math


def run_external_applicaton(command, fail_if_result_not_zero=True):
    current_folder = os.getcwd()
    logging.debug(f"Executing {command} in {current_folder}.")
    result = os.system(command)
    if fail_if_result_not_zero and result != 0:
        logging.fatal(f"Could not execute {command}: {result}.")
        raise RuntimeError
    else:
        return result


def replace_values_in_file(file, replacements):
    for replacement in replacements:
        replace_value_in_file(file, replacement["search_for"], replacement["replace_with"])


def replace_value_in_file(file, search_for, replace_with):
    with open(file, "r") as f:
        content = f.read()
        content = content.replace(search_for, replace_with)
    with open(file, "w") as f:
        f.write(content)
