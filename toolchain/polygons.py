#!/usr/bin/env python3

import os
import argparse
import logging
import sqlite3
import contextlib
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from lib import init_db, get_scalar, execute_statement

def insert_zero_users_record_at_the_beginning(scaled_operational_profile):
    scaled_operational_profile.loc[-1] = [0, 0, 0]
    scaled_operational_profile.index = scaled_operational_profile.index + 1
    scaled_operational_profile.sort_index(inplace=True)
    return scaled_operational_profile

def create_dashboard(project):
    with contextlib.closing(sqlite3.connect("pptam.db")) as connection:
        with connection:
            project_id = get_scalar(connection, "SELECT id FROM projects WHERE name = ?", (project,))
            if project_id is None:
                print("Cannot find project.")
                return

            operational_profile = pd.read_sql(
                """SELECT users, frequency 
                FROM operational_profile_observations 
                WHERE operational_profile = (SELECT id FROM operational_profiles WHERE project = :project) order by users""",
                connection,
                params=(project_id,),
            )

            all_data = pd.read_sql(
                """SELECT tests.id AS test_id, test_sets.id AS test_set_id, CAST(test_properties.value as integer) AS users, metrics.abbreviation AS metric, items.name AS item_name, results.value AS item_value
                FROM results 
                INNER JOIN tests ON results.test = tests.id
                INNER JOIN items ON results.item = items.id
                INNER JOIN test_properties ON (test_properties.test = tests.id AND test_properties.name = 'load')
                INNER JOIN metrics ON results.metric = metrics.id 
                INNER JOIN test_set_tests ON (test_set_tests.test = tests.id)
                INNER JOIN test_sets ON (test_sets.id = test_set_tests.test_set AND test_sets.project = tests.project)
                WHERE tests.project = :project AND metrics.abbreviation IN ('art', 'sdrt', 'mix')""",
                connection,
                params=(project_id,),
            )

            # scale users in operational profile to users in tests
            max_no_of_users = np.max(all_data.users)
            min_no_of_users = np.min(all_data.users)

            max_no_of_requests = np.max(operational_profile.users)
            scale_factor = max_no_of_users / max_no_of_requests
            scaled_user_load = np.floor(operational_profile.users * scale_factor)
            scaled_operational_profile = pd.DataFrame({"users": scaled_user_load, "frequency": operational_profile.frequency})

            # calculate the relative frequencies in the operational profile
            total_number_of_accesses = np.sum(operational_profile.frequency)
            calculate_frequency = lambda x: x / total_number_of_accesses
            scaled_operational_profile["relative_frequency"] = scaled_operational_profile["frequency"].apply(calculate_frequency)

            # calculate bins and sum relative frequencies for each bin
            number_of_bins = 10
            scaled_operational_profile = insert_zero_users_record_at_the_beginning(scaled_operational_profile)
            scaled_operational_profile["workload_range"] = pd.cut(scaled_operational_profile.users, number_of_bins)
            scaled_operational_profile["workload"] = scaled_operational_profile["workload_range"].apply(lambda range: int(range.right))
            bins = scaled_operational_profile[["workload", "relative_frequency"]].groupby(by=["workload"], as_index=False).sum()  

            # calculate threshold
            data_of_min_user = all_data[all_data.users == min_no_of_users]
            threshold = pd.pivot_table(data_of_min_user[["metric", "item_name", "item_value"]], values="item_value", index=["item_name"], columns=["metric"])
            threshold = pd.DataFrame(threshold.to_records())            
            threshold["threshold"] = threshold.art + 3 * threshold.sdrt
            threshold = threshold[["item_name", "threshold"]]

            # list_of_microservices = pd.unique(all_data.item_name)
            tests = pd.pivot_table(all_data[all_data.users != min_no_of_users], values="item_value", index=["test_id", "test_set_id", "users", "item_name"], columns=["metric"], aggfunc=np.mean, fill_value=np.Infinity)
            tests = pd.DataFrame(tests.to_records())             
            tests["relative_mass"] = tests.apply(lambda row: row["mix"] if np.max(threshold[threshold.item_name==row["item_name"]].threshold) > row["art"] else 0, axis = 1)
            tests = tests[["test_id", "test_set_id", "users", "relative_mass"]].groupby(by=["test_id", "test_set_id", "users"], as_index=False).sum()
            tests["absolute_mass"] = tests.apply(lambda row: row["relative_mass"] * np.max(bins[bins.workload==row["users"]].relative_frequency), axis = 1)
            tests=tests.sort_values(by=["test_set_id", "users"])

            # this should be added as a table
            domain_metric_per_test_set = tests[["test_set_id", "absolute_mass"]].groupby(by=["test_set_id"], as_index=False).sum()

            app = dash.Dash()
            fig = go.Figure()

            fig.add_trace(go.Scatter(name="Operational Profile", x=bins["workload"], y=bins["relative_frequency"], fill='tozeroy'))

            test_sets = pd.read_sql(
                """SELECT id, name 
                FROM test_sets 
                WHERE project = :project""",
                connection,
                params=(project_id,),
            )

            for id, group in tests.groupby(by=["test_set_id"]):
                test_set_name=test_sets[test_sets.id==id].name.squeeze()
                print(test_set_name)
                fig.add_trace(go.Scatter(name=test_set_name, x=group["users"], y=group["absolute_mass"], fill='tozeroy'))

            app.layout = html.Div([dcc.Graph(id="polygon-plot", figure=fig)])
            app.run_server(debug=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("project", help="Name of the project to analyze")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    create_dashboard(args.project)
