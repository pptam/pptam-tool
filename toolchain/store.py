#!/usr/bin/env python3

import os
import argparse
import logging
import configparser
import psycopg2
from datetime import datetime
import csv
import uuid
import statistics
import math

def get_scalar(connection, query, parameters):
    with connection.cursor() as cursor:
        cursor.execute(query, parameters)
        records = cursor.fetchone()
        return records[0]

def store_test(test_path):
    logging.info(f"Storing test {test_path}.")

    configuration = configparser.ConfigParser()
    configuration.read([os.path.join(test_path, "configuration.ini")])

    project_name = configuration["CONFIGURATION"]["PROJECT_NAME"]
    test_set_name = configuration["CONFIGURATION"]["TEST_SET_NAME"]
    test_name = configuration["CONFIGURATION"]["TEST_NAME"]
    created_at = datetime.fromtimestamp(float(configuration["CONFIGURATION"]["TIMESTAMP"]))

    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            project_id = get_scalar(connection, "SELECT create_or_get_project(%s);", (project_name, ))
            
            test_id = get_scalar(connection, """                
                    DELETE FROM tests WHERE project = %s AND name = %s;
                    SELECT create_or_get_test(%s, %s, %s);                    
                """, (project_id, test_name, project_id, test_name, created_at))
            logging.debug(f"Adding test with the id {test_id} and name {test_name}.")

            with connection.cursor() as cursor:
                for item in configuration["CONFIGURATION"]:
                    cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, item, configuration["CONFIGURATION"][item]))

                summary_statistics_path = os.path.join(test_path, "result_stats.csv")
                if os.path.exists(summary_statistics_path):
                    logging.debug(f"Reading {summary_statistics_path}.")
                    
                    # Get aggregated values first
                    total_number_of_requests = 0.0
                    with open(summary_statistics_path, newline='') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                        for row in reader:
                            if row["Name"] == "Aggregated":
                                total_number_of_requests = float(row["Request Count"])

                    with open(summary_statistics_path, newline='') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                        for row in reader:
                            if row["Name"] != "Aggregated":
                                if "Request Count" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "rc", float(row["Request Count"]), created_at))
                                if "Failure Count" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "fc", float(row["Failure Count"]), created_at))
                                if "Median Response Time" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "mrt", float(row["Median Response Time"]), created_at))
                                if "Average Response Time" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "art", float(row["Average Response Time"]), created_at))
                                if "Min Response Time" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "minrt", float(row["Min Response Time"]), created_at))
                                if "Max Response Time" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "maxrt", float(row["Max Response Time"]), created_at))
                                if "Average Content Size" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "acs", float(row["Average Content Size"]), created_at))
                                if "Requests/s" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "rps", float(row["Requests/s"]), created_at))
                                if "Failures/s" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "fps", float(row["Failures/s"]), created_at))
                                
                                # https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-14-135
                                q1 = float(row["25%"])
                                q3 = float(row["75%"])
                                estimated_sd = (q3-q1)/1.35
                                cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "sdrt", estimated_sd, created_at))

                                mix = float(row["Request Count"])/total_number_of_requests
                                cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "mix", mix, created_at))

                history_statistics_path = os.path.join(test_path, "result_stats_history.csv")
                if os.path.exists(history_statistics_path):
                    logging.debug(f"Reading {history_statistics_path}.")
                    with open(history_statistics_path, newline='') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                        for row in reader:
                            if row["Name"] != "Aggregated":
                                created_at = datetime.fromtimestamp(int(row["Timestamp"]))
                                if "User Count" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "iuc", float(row["User Count"]), created_at))
                                if "Total Request Count" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "irc", float(row["Total Request Count"]), created_at))
                                if "Total Failure Count" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "ifc", float(row["Total Failure Count"]), created_at))
                                if "Total Median Response Time" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "imrt", float(row["Total Median Response Time"]), created_at))
                                if "Total Average Response Time" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "iart", float(row["Total Average Response Time"]), created_at))
                                if "Total Min Response Time" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "iminrt", float(row["Total Min Response Time"]), created_at))
                                if "Total Max Response Time" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "imaxrt", float(row["Total Max Response Time"]), created_at))
                                if "Total Average Content Size" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "iacs", float(row["Total Average Content Size"]), created_at))
                                if "Requests/s" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "irps", float(row["Requests/s"]), created_at))
                                if "Failures/s" in row:
                                    cursor.execute(f"INSERT INTO results (test, item, metric, value, created_at) VALUES (%s, create_or_get_item('{project_id}', %s), get_metric(%s), %s, %s);", (test_id, row["Name"], "ifps", float(row["Failures/s"]), created_at))                  
                
                if test_set_name!="":
                    logging.debug(f"Assigning test to test set {test_set_name}.")
                    test_set_id = get_scalar(connection, "SELECT create_or_get_test_set(%s, %s);", (project_id, test_set_name))                    
                    cursor.execute("INSERT INTO test_set_tests (test_set, test) VALUES (%s, %s);", (test_set_id, test_id))                  

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stores performed tests in the database.")
    parser.add_argument("test", metavar="path_to_test_results_folder", help="Test results folder")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
        
    if args.test is None or args.test == "" or (not os.path.exists(args.test)):
        logging.fatal(f"Cannot find the test results folder. Please indicate one.")
        quit()

    store_test(args.test)