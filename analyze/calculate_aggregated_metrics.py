#!/usr/bin/env python3

import os
import argparse
import logging
import configparser
import psycopg2
from datetime import datetime
import uuid

def calculate(project):
    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            with connection.cursor() as cursor:      

            









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate aggregated metrics.")
    parser.add_argument("project", help="Project to analize")    
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
        
    calculate(args.project)