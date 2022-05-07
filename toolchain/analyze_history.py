#!/usr/bin/env python3

import os
import argparse
import logging
import contextlib
import sqlite3
from datetime import datetime
import csv
import uuid

def extract():
    
    # SELECT item, value FROM results WHERE metric = 13 median response
    # SELECT item, value FROM results WHERE metric = 14 average response
    # SELECT item, value FROM results WHERE metric = 15 min response
    # SELECT item, value FROM results WHERE metric = 16 max response
    # SELECT item, value FROM results WHERE metric = 11 requests
    # SELECT item, value FROM results WHERE metric = 21 cpu utilization
    # SELECT item, value FROM results WHERE metric = 24 memory utilization

    # instance,counter_name,timestamp,response_time,response_time_max,response_time_min,requests,cpu_utilization_latest,cpu_utilization_max,cpu_utilization_min,ram_utilization_latest,ram_utilization_max,ram_utilization_min,load,provider
    
    starting_metric = 16
    metrics = [13, 14, 15, 16, 11, 21, 24]
    thisdict = {
        "instance": "pptam",
        "counter_name": ,
        "year": 1964
    }

    command = ""
    with contextlib.closing(connection.cursor()) as cursor:
        cursor.execute(command, parameters)
        records = cursor.fetchall()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a dataset consisting of different metrics.")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    extract()