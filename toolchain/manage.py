#!/usr/bin/env python3

import os
import argparse
import logging
import configparser
import psycopg2
from datetime import datetime
import uuid
import sys
from tabulate import tabulate

def get_scalar(command):
    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            with connection.cursor() as cursor:      
                cursor.execute(command)
                record = cursor.fetchone()
                if record is not None:
                    record = record[0]
                return record
    finally:
        if connection is not None:
            connection.close()

def execute_query_with_result(command, headers):
    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            with connection.cursor() as cursor:      
                cursor.execute(command)
                records = cursor.fetchall()
                print("\n" + tabulate(records, headers=headers) + "\n")
    finally:
        if connection is not None:
            connection.close()

def execute_command_without_result(command):
    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            with connection.cursor() as cursor:      
                cursor.execute(command)
                print("")
                
    finally:
        if connection is not None:
            connection.close()

def projects_list(args):
    query = "SELECT id, name FROM projects ORDER BY name"
    headers = ["ID", "Name"]
    execute_query_with_result(query, headers)

def project_create(args):
    query = f"INSERT INTO projects(name) VALUES ('{args.name}')"
    execute_command_without_result(query)

def project_delete(args):
    query = f"DELETE FROM projects WHERE name = '{args.name}'"
    execute_command_without_result(query)

def tests_list(args):
    query = "SELECT tests.id, projects.name, tests.name FROM tests INNER JOIN projects ON tests.project = projects.id WHERE projects.name = '{args.project}' ORDER BY projects.name, tests.name"
    headers = ["ID", "Project", "Name"]
    execute_query_with_result(query, headers)

def test_rename(args):
    query = f"UPDATE tests SET name = '{args.name2}' WHERE name = '{args.name1}' AND project = (SELECT id FROM projects WHERE name = '{args.project}')"
    execute_command_without_result(query)

def test_delete(args):
    query = f"DELETE FROM tests WHERE name = '{args.name}'"
    execute_command_without_result(query)

def test_link(args):
    test_set_id = get_scalar(f"SELECT test_sets.id FROM test_sets INNER JOIN projects ON test_sets.project = projects.id WHERE test_sets.name = '{args.set}' AND projects.name = '{args.project}'")
    if test_set_id is None:
        print("Cannot find test set.")
    else:
        test_id = get_scalar(f"SELECT tests.id FROM tests INNER JOIN projects ON tests.project = projects.id WHERE tests.name = '{args.test}' AND projects.name = '{args.project}'")
        if test_id is None:
            print("Cannot find test.")
        else:
            query = f"INSERT INTO test_set_tests (test_set, test) VALUES ('{test_set_id}', '{test_id}')"
            execute_command_without_result(query)

def profiles_list(args):
    query = f"SELECT operational_profiles.id, projects.name, operational_profiles.name FROM operational_profiles INNER JOIN projects ON operational_profiles.project = projects.id WHERE projects.name = '{args.project}' ORDER BY projects.name, operational_profiles.name"
    headers = ["ID", "Project", "Name"]
    execute_query_with_result(query, headers)

def profile_rename(args):
    query = f"UPDATE operational_profiles SET name = '{args.name2}' WHERE name = '{args.name1}' AND project = (SELECT id FROM projects WHERE name = '{args.project}')"
    execute_command_without_result(query)

def profile_delete(args):
    query = f"DELETE FROM operational_profiles WHERE name = '{args.name}'"
    execute_command_without_result(query)

def sets_list(args):
    query = f"SELECT test_sets.id, projects.name, test_sets.name, count(test_set_tests.id) FROM test_sets LEFT OUTER JOIN test_set_tests ON test_sets.id = test_set_tests.test_set INNER JOIN projects ON test_sets.project = projects.id WHERE projects.name = '{args.project}' GROUP BY test_sets.id, projects.name, test_sets.name ORDER BY test_sets.id, projects.name, test_sets.name"
    headers = ["ID", "Project", "Name", "Tests"]
    execute_query_with_result(query, headers)

def set_create(args):
    project_id = get_scalar(f"SELECT id FROM projects WHERE name = '{args.project}'")
    if project_id is None:
        print("Cannot find project.")
    else:
        query = f"INSERT INTO test_sets (project, name) VALUES ('{project_id}', '{args.name}')"
        execute_command_without_result(query)

def set_rename(args):
    query = f"UPDATE test_sets SET name = '{args.name2}' WHERE name = '{args.name1}' AND project = (SELECT id FROM projects WHERE name = '{args.project}')"
    execute_command_without_result(query)

def set_delete(args):
    query = f"DELETE FROM test_sets WHERE name = '{args.name}'"
    execute_command_without_result(query)

def set_show(args):
    query = f"SELECT tests.id, tests.name FROM tests INNER JOIN projects ON tests.project = projects.id INNER JOIN test_set_tests ON test_set_tests.test = tests.id INNER JOIN test_sets ON test_set_tests.test_set = test_sets.id WHERE projects.name = '{args.project}' AND test_sets.name = '{args.set}' ORDER BY tests.name"
    headers = ["ID", "Name"]
    execute_query_with_result(query, headers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize items stored in the database")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)

    subparsers = parser.add_subparsers(dest="command", required=True, help="One of the following commands:")
    subparser_projects = subparsers.add_parser("projects", help="Manage projects")
    subparser_projects_subparser = subparser_projects.add_subparsers(dest="action", required=True, help="One of the following actions:")
    subparser_projects_subparser_create = subparser_projects_subparser.add_parser("create", help="Create projects")
    subparser_projects_subparser_create.add_argument("name", help="The name of the project")
    subparser_projects_subparser_delete = subparser_projects_subparser.add_parser("delete", help="Delete projects")
    subparser_projects_subparser_delete.add_argument("name", help="The name of the project")
    subparser_projects_subparser_list = subparser_projects_subparser.add_parser("list", help="List projects")

    subparser_profiles = subparsers.add_parser("profiles", help="Manage operational profiles")
    subparser_profiles_subparser = subparser_profiles.add_subparsers(dest="action", required=True, help="One of the following actions:")
    subparser_profiles_subparser_rename = subparser_profiles_subparser.add_parser("rename", help="Rename operational profiles")
    subparser_profiles_subparser_rename.add_argument("project", help="The name of the project")
    subparser_profiles_subparser_rename.add_argument("name1", help="The name of the operational profile to rename")
    subparser_profiles_subparser_rename.add_argument("name2", help="The new name of the operational profile to rename")
    subparser_profiles_subparser_delete = subparser_profiles_subparser.add_parser("delete", help="Delete operational profiles")
    subparser_profiles_subparser_delete.add_argument("project", help="The name of the project")
    subparser_profiles_subparser_delete.add_argument("name", help="The name of the operational profile")
    subparser_profiles_subparser_list = subparser_profiles_subparser.add_parser("list", help="List operational profiles")
    subparser_profiles_subparser_list.add_argument("project", help="The name of the project")

    subparser_sets = subparsers.add_parser("sets", help="Manage test sets")
    subparser_sets_subparser = subparser_sets.add_subparsers(dest="action", required=True, help="One of the following actions:")
    subparser_sets_subparser_rename = subparser_sets_subparser.add_parser("rename", help="Rename test sets")
    subparser_sets_subparser_rename.add_argument("project", help="The name of the project")
    subparser_sets_subparser_rename.add_argument("name1", help="The name of the test set to rename")
    subparser_sets_subparser_rename.add_argument("name2", help="The new name of the test set to rename")
    subparser_sets_subparser_delete = subparser_sets_subparser.add_parser("delete", help="Delete test sets")
    subparser_sets_subparser_delete.add_argument("project", help="The name of the project")
    subparser_sets_subparser_delete.add_argument("name", help="The name of the test set")
    subparser_sets_subparser_list = subparser_sets_subparser.add_parser("list", help="List test sets")
    subparser_sets_subparser_list.add_argument("project", help="The name of the project")
    subparser_sets_subparser_create = subparser_sets_subparser.add_parser("create", help="Create test sets")
    subparser_sets_subparser_create.add_argument("project", help="The name of the project")
    subparser_sets_subparser_create.add_argument("name", help="The name of the test set")
    subparser_sets_subparser_show = subparser_sets_subparser.add_parser("show", help="Show tests within a test set")
    subparser_sets_subparser_show.add_argument("project", help="The name of the project")
    subparser_sets_subparser_show.add_argument("set", help="The name of the test set")

    subparser_tests = subparsers.add_parser("tests", help="Manage tests")
    subparser_tests_subparser = subparser_tests.add_subparsers(dest="action", required=True, help="One of the following actions:")
    subparser_tests_subparser_rename = subparser_tests_subparser.add_parser("rename", help="Rename tests")
    subparser_tests_subparser_rename.add_argument("project", help="The name of the project")
    subparser_tests_subparser_rename.add_argument("name1", help="The name of the test to rename")
    subparser_tests_subparser_rename.add_argument("name2", help="The new name of the test to rename")
    subparser_tests_subparser_delete = subparser_tests_subparser.add_parser("delete", help="Delete tests")
    subparser_tests_subparser_delete.add_argument("project", help="The name of the project")
    subparser_tests_subparser_delete.add_argument("name", help="The name of the test")
    subparser_tests_subparser_list = subparser_tests_subparser.add_parser("list", help="List tests")
    subparser_tests_subparser_list.add_argument("project", help="The name of the project")
    subparser_tests_subparser_link = subparser_tests_subparser.add_parser("link", help="Link tests to test sets")
    subparser_tests_subparser_link.add_argument("project", help="The name of the project")
    subparser_tests_subparser_link.add_argument("test", help="The name of the test")
    subparser_tests_subparser_link.add_argument("set", help="The name of the test set")

    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    switcher = {
        "projects_list": projects_list,
        "projects_create": project_create,
        "projects_delete": project_delete,  
        "profiles_list": profiles_list,
        "profiles_rename": profile_rename,
        "profiles_delete": profile_delete,
        "sets_list": sets_list,
        "sets_rename": set_rename,
        "sets_delete": set_delete,
        "sets_create": set_create,
        "sets_show": set_show,
        "tests_list": tests_list,
        "tests_rename": test_rename,
        "tests_delete": test_delete,
        "tests_link": test_link
    }

    switcher.get(args.command + "_" + args.action)(args)





    