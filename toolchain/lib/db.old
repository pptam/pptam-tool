#!/usr/bin/env python
import sqlite3
import contextlib
import uuid


def execute_statement(connection, statement, parameters=()):
    with contextlib.closing(connection.cursor()) as cursor:
        cursor.execute(statement, parameters)


def get_scalar(connection, statement, parameters=()):
    with contextlib.closing(connection.cursor()) as cursor:
        cursor.execute(statement, parameters)
        result = cursor.fetchone()
        if result is None:
            return None
        
        return result[0]


def create_or_get_item(connection, project, name):
    execute_statement(connection, "INSERT OR IGNORE INTO items (id, project, name) VALUES (?, ?, ?);", (str(uuid.uuid4()), project, name))
    return get_scalar(connection, "SELECT id FROM items WHERE project = ? AND name = ?;", (project, name))


def create_or_get_project(connection, name):
    execute_statement(connection, "INSERT OR IGNORE INTO projects (id, name) VALUES (?, ?);", (str(uuid.uuid4()), name))
    return get_scalar(connection, "SELECT id FROM projects WHERE name = ?;", (name, ))


def create_or_get_test(connection, project, name, created_at):
    execute_statement(connection, "INSERT OR IGNORE INTO tests (id, project, name, created_at) VALUES (?, ?, ?, ?);", (str(uuid.uuid4()), project, name, created_at))
    return get_scalar(connection, "SELECT id FROM tests WHERE project = ? AND name = ?;", (project, name))


def create_or_get_test_set(connection, project, name):
    execute_statement(connection, "INSERT OR IGNORE INTO test_sets (id, project, name) VALUES (?, ?, ?);", (str(uuid.uuid4()), project, name))
    return get_scalar(connection, "SELECT id FROM test_sets WHERE project = ? AND name = ?;", (project, name))


def get_metric(connection, name):
    return get_scalar(connection, "SELECT id FROM metrics WHERE abbreviation = ?;", (name, ))


def init_db():
    with contextlib.closing(sqlite3.connect("pptam.db")) as connection:
        with connection:
            execute_statement(connection, "DROP TABLE IF EXISTS test_set_tests;")
            execute_statement(connection, "DROP TABLE IF EXISTS test_set_properties;")
            execute_statement(connection, "DROP TABLE IF EXISTS test_sets;")
            execute_statement(connection, "DROP TABLE IF EXISTS operational_profile_observations;")
            execute_statement(connection, "DROP TABLE IF EXISTS operational_profiles;")
            execute_statement(connection, "DROP TABLE IF EXISTS result_properties;")
            execute_statement(connection, "DROP TABLE IF EXISTS results;")
            execute_statement(connection, "DROP TABLE IF EXISTS test_properties;")
            execute_statement(connection, "DROP TABLE IF EXISTS tests;")
            execute_statement(connection, "DROP TABLE IF EXISTS project_properties;")
            execute_statement(connection, "DROP TABLE IF EXISTS item_item_properties;")
            execute_statement(connection, "DROP TABLE IF EXISTS item_items;")
            execute_statement(connection, "DROP TABLE IF EXISTS item_properties;")
            execute_statement(connection, "DROP TABLE IF EXISTS items;")
            execute_statement(connection, "DROP TABLE IF EXISTS projects;")
            execute_statement(connection, "DROP TABLE IF EXISTS metrics;")
            execute_statement(connection, "DROP TABLE IF EXISTS relations;")

            execute_statement(connection, "CREATE TABLE IF NOT EXISTS metrics (id integer NOT NULL, name text NOT NULL, abbreviation text NOT NULL, created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT metric_pkey PRIMARY KEY (id), CONSTRAINT metrics_name_unique UNIQUE (name), CONSTRAINT metrics_abbreviation_unique UNIQUE (abbreviation))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS relations (id integer NOT NULL, name text NOT NULL, abbreviation text NOT NULL, created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT relation_pkey PRIMARY KEY (id), CONSTRAINT relations_name_unique UNIQUE (name), CONSTRAINT relations_abbreviation_unique UNIQUE (abbreviation))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS projects (id text NOT NULL, name text, created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT project_pkey PRIMARY KEY (id), CONSTRAINT projects_name_unique UNIQUE (name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS project_properties (id text NOT NULL, project text NOT NULL, name text NOT NULL, value text NOT NULL, CONSTRAINT project_properties_pkey PRIMARY KEY (id), CONSTRAINT project_fkey FOREIGN KEY (project) REFERENCES projects(id) ON DELETE CASCADE, CONSTRAINT project_properties_name_unique UNIQUE (project, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS tests (id text NOT NULL, project text NOT NULL, name text NOT NULL, created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT tests_pkey PRIMARY KEY (id), CONSTRAINT project_fkey FOREIGN KEY (project) REFERENCES projects(id) ON DELETE CASCADE, CONSTRAINT tests_name_unique UNIQUE (project, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS test_properties (id text NOT NULL, test text NOT NULL, name text NOT NULL, value text NOT NULL, CONSTRAINT test_properties_pkey PRIMARY KEY (id), CONSTRAINT test_fkey FOREIGN KEY (test) REFERENCES tests(id) ON DELETE CASCADE, CONSTRAINT test_properties_name_unique UNIQUE (test, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS test_sets (id text NOT NULL, project text NOT NULL, name text NOT NULL, CONSTRAINT test_tests_pkey PRIMARY KEY (id), CONSTRAINT project_fkey FOREIGN KEY (project) REFERENCES projects(id) ON DELETE CASCADE, CONSTRAINT test_sets_name_unique UNIQUE (project, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS test_set_properties (id text NOT NULL, test_set text NOT NULL, name text NOT NULL, value text NOT NULL, CONSTRAINT test_set_properties_pkey PRIMARY KEY (id), CONSTRAINT test_set_fkey FOREIGN KEY (test_set) REFERENCES test_sets(id) ON DELETE CASCADE, CONSTRAINT test_set_properties_name_unique UNIQUE (test_set, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS test_set_tests (id text NOT NULL, test_set text NOT NULL, test text NOT NULL, CONSTRAINT test_set_tests_pkey PRIMARY KEY (id), CONSTRAINT test_set_fkey FOREIGN KEY (test_set) REFERENCES test_sets(id) ON DELETE CASCADE, CONSTRAINT test_fkey FOREIGN KEY (test) REFERENCES tests(id) ON DELETE CASCADE, CONSTRAINT test_set_tests_unique UNIQUE (test_set, test))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS items (id text NOT NULL, project text NOT NULL, name text, created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT items_pkey PRIMARY KEY (id), CONSTRAINT project_fkey FOREIGN KEY (project) REFERENCES projects(id) ON DELETE CASCADE, CONSTRAINT items_name_unique UNIQUE (project, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS item_properties (id text NOT NULL, item text NOT NULL, name text NOT NULL, value text NOT NULL, CONSTRAINT item_properties_pkey PRIMARY KEY (id), CONSTRAINT item_fkey FOREIGN KEY (item) REFERENCES items(id) ON DELETE CASCADE, CONSTRAINT item_properties_name_unique UNIQUE (item, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS item_items (id text NOT NULL, item1 text NOT NULL, item2 text NOT NULL, relation integer NOT NULL, created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT item_items_pkey PRIMARY KEY (id), CONSTRAINT item1_fkey FOREIGN KEY (item1) REFERENCES items(id) ON DELETE CASCADE, CONSTRAINT item2_fkey FOREIGN KEY (item2) REFERENCES items(id) ON DELETE CASCADE, CONSTRAINT relation_fkey FOREIGN KEY (relation) REFERENCES relations(id) ON DELETE CASCADE, CONSTRAINT item_items_unique UNIQUE (item1, item2))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS item_item_properties (id text NOT NULL, item_item text NOT NULL, name text NOT NULL, value text NOT NULL, CONSTRAINT item_item_properties_pkey PRIMARY KEY (id), CONSTRAINT item_item_fkey FOREIGN KEY (item_item) REFERENCES item_items(id) ON DELETE CASCADE, CONSTRAINT item_item_properties_name_unique UNIQUE (item_item, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS results (id text NOT NULL, test text NOT NULL, item text NOT NULL, metric integer NOT NULL, value float NOT NULL, created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT results_pkey PRIMARY KEY (id), CONSTRAINT test_fkey FOREIGN KEY (test) REFERENCES tests(id) ON DELETE CASCADE, CONSTRAINT item_fkey FOREIGN KEY (item) REFERENCES items(id) ON DELETE CASCADE, CONSTRAINT metric_fkey FOREIGN KEY (metric) REFERENCES metrics(id) ON DELETE NO ACTION);")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS result_properties (id text NOT NULL, result text NOT NULL, name text NOT NULL, value text NOT NULL, CONSTRAINT result_properties_pkey PRIMARY KEY (id), CONSTRAINT result_fkey FOREIGN KEY (result) REFERENCES results(id) ON DELETE CASCADE, CONSTRAINT result_properties_name_unique UNIQUE (result, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS operational_profiles (id text NOT NULL, project text NOT NULL, name text NOT NULL, created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT operational_profiles_pkey PRIMARY KEY (id), CONSTRAINT project_fkey FOREIGN KEY (project) REFERENCES projects(id) ON DELETE CASCADE, CONSTRAINT operational_profiles_name_unique UNIQUE (project, name))")
            execute_statement(connection, "CREATE TABLE IF NOT EXISTS operational_profile_observations (id text NOT NULL, operational_profile text NOT NULL, users integer NOT NULL, frequency integer NOT NULL, CONSTRAINT operational_profile_observations_pkey PRIMARY KEY (id), CONSTRAINT operational_profile_fkey FOREIGN KEY (operational_profile) REFERENCES operational_profiles(id) ON DELETE CASCADE, CONSTRAINT operational_profile_observations_unique UNIQUE (operational_profile, users, frequency))")

            execute_statement(connection, "CREATE INDEX items_name ON items (project, name);")

            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (1, 'Request count', 'rc');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (2, 'Failure count', 'fc');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (3, 'Median response time in seconds', 'mrt');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (4, 'Average response time in seconds', 'art');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (5, 'Min response time in seconds', 'minrt');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (6, 'Max response time in seconds', 'maxrt');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (7, 'Average content size', 'acs');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (8, 'Requests per second', 'rps');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (9, 'Failures per second', 'fps');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (10, 'Intermediate user count', 'iuc');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (11, 'Intermediate request count', 'irc');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (12, 'Intermediate failure count', 'ifc');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (13, 'Intermediate median response time in seconds', 'imrt');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (14, 'Intermediate average response time in seconds', 'iart');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (15, 'Intermediate min response time in seconds', 'iminrt');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (16, 'Intermediate max response time in seconds', 'imaxrt');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (17, 'Intermediate average content size', 'iacs');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (18, 'Intermediate requests per second', 'irps');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (19, 'Intermediate failures per second', 'ifps');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (20, 'Memory utilization in percent', 'mup');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (21, 'CPU utilization in percent', 'cup');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (22, 'Standard deviation of response time in seconds', 'sdrt');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (23, 'Mix in percent', 'mix');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (24, 'Memory utilization', 'mut');")
            execute_statement(connection, "INSERT INTO metrics (id, name, abbreviation) VALUES (25, 'Memory limit', 'mel');")

            execute_statement(connection, "INSERT INTO relations (id, name, abbreviation) VALUES (1, 'Call', 'c');")
            execute_statement(connection, "INSERT INTO relations (id, name, abbreviation) VALUES (2, 'Part of', 'p');")
