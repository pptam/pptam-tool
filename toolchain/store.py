#!/usr/bin/env python3

import os
import argparse
import logging
import configparser
import contextlib
import sqlite3
from datetime import datetime
import csv
import uuid
from lib import init_db, execute_statement, create_or_get_item, create_or_get_project, create_or_get_test, create_or_get_test_set, get_metric
import math


def store_test(test_path):
    logging.info(f"Storing test {test_path}.")

    configuration = configparser.ConfigParser()
    configuration.read([os.path.join(test_path, "configuration.ini")])

    project_name = configuration["CONFIGURATION"]["PROJECT_NAME"]
    test_set_name = configuration["CONFIGURATION"]["TEST_SET_NAME"]
    test_name = configuration["CONFIGURATION"]["TEST_NAME"]
    created_at = datetime.fromtimestamp(math.trunc(float(configuration["CONFIGURATION"]["TIMESTAMP"])))

    if not os.path.exists("pptam.db"):
        logging.debug(f"Creating database since pptam.db does not exist.")
        init_db()

    with contextlib.closing(sqlite3.connect("pptam.db")) as connection:
        with connection:
            project_id = create_or_get_project(connection, project_name)

            execute_statement(connection, "DELETE FROM tests WHERE project = ? AND name = ?;", (project_id, test_name))
            test_id = create_or_get_test(connection, project_id, test_name, created_at)

            logging.debug(f"Adding test with the id {test_id} and name {test_name}.")

            for item in configuration["CONFIGURATION"]:
                execute_statement(connection, "INSERT INTO test_properties (id, test, name, value) VALUES (?, ?, ?, ?);", (str(uuid.uuid4()), test_id, item, configuration["CONFIGURATION"][item]))

            summary_statistics_path = os.path.join(test_path, "result_stats.csv")
            if os.path.exists(summary_statistics_path):
                logging.debug(f"Reading {summary_statistics_path}.")

                # Get aggregated values first
                total_number_of_requests = 0.0
                with open(summary_statistics_path, newline="") as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                    for row in reader:
                        if row["Name"] == "Aggregated":
                            total_number_of_requests = float(row["Request Count"])

                with open(summary_statistics_path, newline="") as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                    for row in reader:
                        if row["Name"] != "Aggregated":
                            if "Request Count" in row and row["Request Count"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "rc"), float(row["Request Count"]), created_at))

                                mix = float(row["Request Count"]) / total_number_of_requests
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "mix"), mix, created_at))

                            if "Failure Count" in row and row["Failure Count"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "fc"), float(row["Failure Count"]), created_at))
                            if "Median Response Time" in row and row["Median Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "mrt"), float(row["Median Response Time"]), created_at))
                            if "Average Response Time" in row and row["Average Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "art"), float(row["Average Response Time"]), created_at))
                            if "Min Response Time" in row and row["Min Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "minrt"), float(row["Min Response Time"]), created_at))
                            if "Max Response Time" in row and row["Max Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "maxrt"), float(row["Max Response Time"]), created_at))
                            if "Average Content Size" in row and row["Average Content Size"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "acs"), float(row["Average Content Size"]), created_at))
                            if "Requests/s" in row and row["Requests/s"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "rps"), float(row["Requests/s"]), created_at))
                            if "Failures/s" in row and row["Failures/s"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "fps"), float(row["Failures/s"]), created_at))
                            if "Standard Deviation Response Time" in row and row["Standard Deviation Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "sdrt"), float(row["Standard Deviation Response Time"]), created_at))
                            else:
                                if row["25%"] != "N/A" and row["75%"] != "N/A":
                                    # https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-14-135
                                    q1 = float(row["25%"])
                                    q3 = float(row["75%"])
                                    estimated_sd = (q3 - q1) / 1.35
                                    execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "sdrt"), estimated_sd, created_at))

            history_statistics_path = os.path.join(test_path, "result_stats_history.csv")
            if os.path.exists(history_statistics_path):
                logging.debug(f"Reading {history_statistics_path}.")
                with open(history_statistics_path, newline="") as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                    for row in reader:
                        if row["Name"] != "Aggregated":
                            created_at = datetime.fromtimestamp(int(row["Timestamp"]))
                            if "User Count" in row and row["User Count"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "iuc"), float(row["User Count"]), created_at))
                            if "Total Request Count" in row and row["Total Request Count"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "irc"), float(row["Total Request Count"]), created_at))
                            if "Total Failure Count" in row and row["Total Failure Count"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "ifc"), float(row["Total Failure Count"]), created_at))
                            if "Total Median Response Time" in row and row["Total Median Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "imrt"), float(row["Total Median Response Time"]), created_at))
                            if "Total Average Response Time" in row and row["Total Average Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "iart"), float(row["Total Average Response Time"]), created_at))
                            if "Total Min Response Time" in row and row["Total Min Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "iminrt"), float(row["Total Min Response Time"]), created_at))
                            if "TotalMax Response Time" in row and row["TotalMax Response Time"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "imaxrt"), float(row["TotalMax Response Time"]), created_at))
                            if "Total Average Content Size" in row and row["Total Average Content Size"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "iacs"), float(row["Total Average Content Size"]), created_at))
                            if "Requests/s" in row and row["Requests/s"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "irps"), float(row["Requests/s"]), created_at))
                            if "Failures/s" in row and row["Failures/s"] != "N/A":
                                execute_statement(connection, f"INSERT INTO results (id, test, item, metric, value, created_at) VALUES (?, ?, ?, ?, ?, ?);", (str(uuid.uuid4()), test_id, create_or_get_item(connection, project_id, row["Name"]), get_metric(connection, "ifps"), float(row["Failures/s"]), created_at))

            if test_set_name != "":
                logging.debug(f"Assigning test to test set {test_set_name}.")
                test_set_id = create_or_get_test_set(connection, project_id, test_set_name)
                execute_statement(connection, "INSERT INTO test_set_tests (id, test_set, test) VALUES (?, ?, ?);", (str(uuid.uuid4()), test_set_id, test_id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stores performed tests in the database.")
    parser.add_argument("test", metavar="path_to_test_results_folder", help="Test results folder")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    if args.test is None or args.test == "" or (not os.path.exists(args.test)):
        logging.fatal(f"Cannot find the test results folder. Please indicate one.")
        quit()

    store_test(args.test)
