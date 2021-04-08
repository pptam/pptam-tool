#!/usr/bin/env python3

import os
import argparse
import logging
import configparser
import psycopg2
from datetime import datetime
import csv
import uuid

def get_scalar(connection, query, parameters):
    with connection.cursor() as cursor:
        cursor.execute(query, parameters)
        records = cursor.fetchone()
        return records[0]

def store_test(file_to_import):
    logging.info(f"Importing file {file_to_import}.")

    project_id = "1628ba4d-8900-41a6-88a3-2c0868b53566"

    test_id = None

    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        current_id = 0
        
        with connection:
            with connection.cursor() as cursor:      
                skip_first_line = False
                with open(file_to_import, newline='') as csvfile:
                    if "sep=" in csvfile.read():
                        skip_first_line = True

                with open(file_to_import, newline='') as csvfile:
                    if skip_first_line:
                        csvfile.__next__()

                    # Read CSV file
                    reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
                    for row in reader:
                        id = int(row["ID"])
                        if id!=current_id:
                            current_id = id
                            test_id = str(uuid.uuid4())
                            logging.info(f"Switching to test id {test_id}.")

                            test_name = row["Memory"] + "mb_" + row["CPU"] + "cpu_" + row["CartReplicas"] + "cart_replicas (" + row["ID"] + ")"
                            cursor.execute("INSERT INTO tests (id, project, name) VALUES (%s, %s, %s);", (test_id, project_id, test_name))
                            
                        cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, "no_of_users", row["Users"]))
                        cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, "memory", row["Memory"]))
                        cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, "cpu", row["CPU"]))
                        cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, "cart_replicas", row["CartReplicas"]))
                            
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "createOrder", 4, float(row["createOrder"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "basket", 4, float(row["basket"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCatalogue", 4, float(row["getCatalogue"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getItem", 4, float(row["getItem"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCart", 4, float(row["getCart"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "login", 4, float(row["login"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getOrders", 4, float(row["getOrders"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "catalogue", 4, float(row["catalogue"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "home", 4, float(row["home"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "tags", 4, float(row["tags"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCustomer", 4, float(row["getCustomer"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "viewOrdersPage", 4, float(row["viewOrdersPage"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "cataloguePage", 4, float(row["cataloguePage"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getRelated", 4, float(row["getRelated"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "addToCart", 4, float(row["addToCart"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "catalogueSize", 4, float(row["catalogueSize"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getAddress", 4, float(row["getAddress"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCard", 4, float(row["getCard"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "showDetails", 4, float(row["showDetails"])))                    
                        row = reader.__next__()
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "createOrder", 22, float(row["createOrder"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "basket", 22, float(row["basket"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCatalogue", 22, float(row["getCatalogue"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getItem", 22, float(row["getItem"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCart", 22, float(row["getCart"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "login", 22, float(row["login"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getOrders", 22, float(row["getOrders"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "catalogue", 22, float(row["catalogue"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "home", 22, float(row["home"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "tags", 22, float(row["tags"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCustomer", 22, float(row["getCustomer"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "viewOrdersPage", 22, float(row["viewOrdersPage"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "cataloguePage", 22, float(row["cataloguePage"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getRelated", 22, float(row["getRelated"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "addToCart", 22, float(row["addToCart"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "catalogueSize", 22, float(row["catalogueSize"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getAddress", 22, float(row["getAddress"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCard", 22, float(row["getCard"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "showDetails", 22, float(row["showDetails"])))                    
                        row = reader.__next__()
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "createOrder", 23, float(row["createOrder"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "basket", 23, float(row["basket"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCatalogue", 23, float(row["getCatalogue"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getItem", 23, float(row["getItem"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCart", 23, float(row["getCart"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "login", 23, float(row["login"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getOrders", 23, float(row["getOrders"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "catalogue", 23, float(row["catalogue"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "home", 23, float(row["home"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "tags", 23, float(row["tags"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCustomer", 23, float(row["getCustomer"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "viewOrdersPage", 23, float(row["viewOrdersPage"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "cataloguePage", 23, float(row["cataloguePage"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getRelated", 23, float(row["getRelated"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "addToCart", 23, float(row["addToCart"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "catalogueSize", 23, float(row["catalogueSize"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getAddress", 23, float(row["getAddress"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "getCard", 23, float(row["getCard"])))
                        cursor.execute("INSERT INTO results(test, object_of_study, metric, value) VALUES (%s, %s, %s, %s);", (test_id, "showDetails", 23, float(row["showDetails"])))                    
                        
    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Imports old experiments.")
    parser.add_argument("file", help="File to import")    
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
        
    store_test(args.file)