#!/usr/bin/env python
import sys
import logging
import os
from time import sleep
import math


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = "=" * filled_len + "-" * (bar_len - filled_len)
    sys.stdout.write("[%s] %s%s %s\r" % (bar, percents, '%', suffix))
    sys.stdout.flush()


def run_external_applicaton(command, fail_if_result_not_zero=True):
    current_folder = os.getcwd()
    logging.debug(f"Executing {command} in {current_folder}.")
    result = os.system(command)
    if fail_if_result_not_zero and result != 0:
        logging.fatal(f"Could not execute {command}.")
        raise RuntimeError


def wait(seconds_to_wait, maximum, information, time_already_elapsed, progress_maximum=math.inf):
    count = 0
    while count < seconds_to_wait:
        progress(min(maximum, progress_maximum, time_already_elapsed + count), maximum, information)
        count += 1
        sleep(1)
