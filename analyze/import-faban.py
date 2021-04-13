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
                            logging.debug(f"Importing test {test_id}.")

                            test_name = row["Memory"] + "mb_" + row["CPU"] + "cpu_" + row["CartReplicas"] + "cart_replicas (" + row["ID"] + ")"
                            cursor.execute("INSERT INTO tests (id, project, name) VALUES (%s, %s, %s);", (test_id, project_id, test_name))
                            
                        cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, "no_of_users", row["Users"]))
                        cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, "memory", row["Memory"]))
                        cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, "cpu", row["CPU"]))
                        cursor.execute("INSERT INTO test_properties (test, name, value) VALUES (%s, %s, %s);", (test_id, "cart_replicas", row["CartReplicas"]))
                        
                        fields = ["createOrder", "basket", "getCatalogue", "getItem", "getCart", "login", "getOrders", "catalogue", "home", "tags", "getCustomer", "viewOrdersPage", "cataloguePage", "getRelated", "addToCart", "catalogueSize", "getAddress", "getCard", "showDetails"]

                        for field in fields:
                            cursor.execute(f"INSERT INTO results(test, item, metric, value) VALUES (%s, create_or_get_item('{project_id}', %s), %s, %s);", (test_id, field, 4, float(row[field])))                                                    

                        row = reader.__next__()
                        
                        for field in fields:
                            cursor.execute(f"INSERT INTO results(test, item, metric, value) VALUES (%s, create_or_get_item('{project_id}', %s), %s, %s);", (test_id, field, 22, float(row[field])))
                        
                        row = reader.__next__()
                        
                        for field in fields:
                            cursor.execute(f"INSERT INTO results(test, item, metric, value) VALUES (%s, create_or_get_item('{project_id}', %s), %s, %s);", (test_id, field, 23, float(row[field])))
            
            with connection.cursor() as cursor: 
                sql_groups = """
                    SELECT A.value::text AS cpu, B.value::text AS memory, C.value::text AS cart_replicas FROM TESTS 
                    INNER JOIN TEST_PROPERTIES A ON (TESTS.ID = A.TEST AND A.name='cpu')
                    INNER JOIN TEST_PROPERTIES B ON (TESTS.ID = B.TEST AND B.name='memory')
                    INNER JOIN TEST_PROPERTIES C ON (TESTS.ID = C.TEST AND C.name='cart_replicas')
                    WHERE TESTS.project=%s
                    GROUP BY cpu, memory, cart_replicas
                    """

                cursor.execute(sql_groups, (project_id, ))
                records = cursor.fetchall()
                
                for test_set in records: 
                    cpu=test_set[0]
                    memory=test_set[1]
                    cart_replicas=test_set[2]
                    
                    test_set_id = str(uuid.uuid4())                    
                    test_set_name = memory + "mb_" + cpu + "cpu_" + cart_replicas + "cart_replicas"
                    logging.debug(f"Creating test set {test_set_id} with name {test_set_name}.")
                    cursor.execute("INSERT INTO test_sets (id, project, name) VALUES (%s, %s, %s);", (test_set_id, project_id, test_set_name))

                    sql_test_set_tests = """
                        SELECT id FROM (SELECT TESTS.id, A.value::text AS cpu, B.value::text AS memory, C.value::text AS cart_replicas FROM TESTS 
                        INNER JOIN TEST_PROPERTIES A ON (TESTS.ID = A.TEST AND A.name='cpu')
                        INNER JOIN TEST_PROPERTIES B ON (TESTS.ID = B.TEST AND B.name='memory')
                        INNER JOIN TEST_PROPERTIES C ON (TESTS.ID = C.TEST AND C.name='cart_replicas') 
                        WHERE TESTS.project=%s) AS A WHERE cpu=%s AND memory=%s AND cart_replicas=%s
                        """

                    with connection.cursor() as cursor2: 
                        cursor2.execute(sql_test_set_tests, (project_id, cpu, memory, cart_replicas))
                        tests = cursor2.fetchall()

                        for test in tests: 
                            test_to_link = test[0]
                            logging.debug(f"Linking test {test_to_link} to it.")
                            cursor.execute("INSERT INTO test_set_tests(test_set, test) VALUES (%s, %s);", (test_set_id, test_to_link))
     
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