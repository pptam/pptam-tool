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

def list(args):
    queries = {
        "projects" : "SELECT id, name FROM projects" + (f" WHERE projects.name = '{args.project}'" if args.project!=None else "") + " ORDER BY name",
        "tests" : "SELECT tests.id, projects.name, tests.name FROM tests INNER JOIN projects ON tests.project = projects.id" + (f" WHERE projects.name = '{args.project}'" if args.project!=None else "") + " ORDER BY projects.name, tests.name",
        "profiles" : "SELECT profiles.id, projects.name, operational_profiles.name FROM operational_profiles INNER JOIN projects ON operational_profiles.project = projects.id" + (f" WHERE projects.name = '{args.project}'" if args.project!=None else "") + " ORDER BY projects.name, operational_profiles.name",
        "sets" : "SELECT test_sets.id, projects.name, test_sets.name, count(test_set_tests.id) FROM test_sets INNER JOIN test_set_tests ON test_sets.id = test_set_tests.test_set INNER JOIN projects ON test_sets.project = projects.id" + (f" WHERE projects.name = '{args.project}'" if args.project!=None else "") + " GROUP BY projects.name, test_sets.name ORDER BY projects.name, test_sets.name"
    } 
    headers = {
        "projects" : ["ID", "Name"],
        "tests": ["ID", "Project", "Name"],
        "profiles": ["ID", "Project", "Name"],
        "sets" : ["ID", "Project", "Name", "Tests"]
    }

    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            with connection.cursor() as cursor:      
                cursor.execute(queries.get(args.type))
                records = cursor.fetchall()
                print("\n" + tabulate(records, headers=headers.get(args.type)) + "\n")
    finally:
        if connection is not None:
            connection.close()

def delete(args):
    queries = {
        "project" : f"DELETE FROM projects WHERE name = '{args.name}'",
        "test" : f"DELETE FROM tests WHERE name = '{args.name}'",
        "profile" : f"DELETE FROM operational_profiles WHERE name = '{args.name}'",
        "set" : f"DELETE FROM test_sets WHERE name = '{args.name}'"
    } 

    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            with connection.cursor() as cursor:      
                cursor.execute(queries.get(args.type))
                print("")
                
    finally:
        if connection is not None:
            connection.close()

def create(args):
    queries = {
        "project" : f"INSERT INTO projects (name) VALUES ('{args.name}');",      
        "set" : f"INSERT INTO test_sets (project, name) VALUES ('{args.name}');",        
    } 

    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            with connection.cursor() as cursor:      
                cursor.execute(queries.get(args.type))
                print("")
                
    finally:
        if connection is not None:
            connection.close()

def link(args):
    queries = {
        "test" : f"INSERT INTO projects(name) VALUES ('{args.name}');",        
    } 


# INSERT INTO public.test_set_tests(test_set, test) VALUES (?, ?, ?);

    connection = None
    try:
        connection = psycopg2.connect(host="localhost", port=5432, dbname="pptam", user="postgres", password="postgres")
        
        with connection:
            with connection.cursor() as cursor:      
                cursor.execute(queries.get(args.type))
                print("")
                
    finally:
        if connection is not None:
            connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize items stored in the database")
    parser.add_argument("action", choices=["create", "delete", "list", "link"], help="The action to perform")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    
    command_parser = parser.add_subparsers(dest="command", required=True, metavar="command", help="One of the following commands:")
    
    parser_list = command_parser.add_parser("list", help="Show items")
    parser_list.add_argument("type", choices=["projects", "tests", "profiles", "sets"], help="The type of item")
    

    

    # parser_delete = command_parser.add_parser("delete", help="Deletes items")
    # parser_delete.add_argument("type", choices=["project", "test", "profile", "set"], help="The type of item")
    # parser_delete.add_argument("name", help="The name of the item to delete")

    # parser_create = command_parser.add_parser("create", help="Creates items")
    # parser_create.add_argument("type", choices=["project"], help="The type of item")
    # parser_create.add_argument("name", help="The name of the item to create")
   
    # parser_link = command_parser.add_parser("link", help="Links items")
    # parser_link.add_argument("type", choices=["test"], help="The type of item")
    # parser_link.add_argument("item1", help="The first item to link")
    # parser_link.add_argument("item2", help="The second item to link")

    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    switcher = {
        "list": list,
        "delete": delete,
        "create": create,
        "link": link
    }

    switcher.get(args.command)(args)





    