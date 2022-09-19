#!/usr/bin/env python3

import argparse
import logging
import sqlite3
import contextlib
import pandas as pd
import numpy as np
from scipy.stats import poisson
import logging
import os
from lib import init_db, get_scalar, execute_statement
import csv
from datetime import datetime

def insert_zero_users_record_at_the_beginning(scaled_operational_profile):
    scaled_operational_profile.loc[-1] = [0, 0, 0]
    scaled_operational_profile.index = scaled_operational_profile.index + 1
    scaled_operational_profile.sort_index(inplace=True)
    return scaled_operational_profile


def create_dashboard(project, threshold_metric, operational_profile_type):
    with contextlib.closing(sqlite3.connect("pptam.db")) as connection:
        with connection:
            project_id = get_scalar(connection, "SELECT id FROM projects WHERE name = ?", (project,))
            if project_id is None:
                logging.error(f"Cannot find project {project}.")
                return
            
            all_data = pd.read_sql(
                """SELECT tests.id AS test_id, test_sets.id AS test_set_id, CAST(test_properties.value as integer) AS users, metrics.abbreviation AS metric, items.name AS item_name, results.value AS item_value
                FROM results 
                INNER JOIN tests ON results.test = tests.id
                INNER JOIN items ON results.item = items.id
                INNER JOIN test_properties ON (test_properties.test = tests.id AND test_properties.name = 'load')
                INNER JOIN metrics ON results.metric = metrics.id 
                INNER JOIN test_set_tests ON (test_set_tests.test = tests.id)
                INNER JOIN test_sets ON (test_sets.id = test_set_tests.test_set AND test_sets.project = tests.project)
                WHERE tests.project = :project AND metrics.abbreviation IN ('art', 'sdrt', 'mix', 'maxrt')""",
                connection,
                params=(project_id,),
            )

            workloads = pd.unique(all_data.sort_values(by="users").users)
            
            binned_operational_profile = None
            
            if operational_profile_type == 1:
                arrival_rate_per_second = 0.017
                time_in_seconds = 3600
                steps = 5
                binned_operational_profile = get_poisson_operational_profile(workloads, arrival_rate_per_second, time_in_seconds, steps)

            if operational_profile_type == 2:
                operational_profile = pd.read_sql(
                    """SELECT users, frequency 
                    FROM operational_profile_observations 
                    WHERE operational_profile = (SELECT id FROM operational_profiles WHERE project = :project) order by users""",
                    connection,
                    params=(project_id,),
                )
                binned_operational_profile = get_predifined_operational_profile(operational_profile, all_data, workloads)

            # calculate threshold
            min_no_of_users = np.min(all_data.users)
            data_of_min_user = all_data[all_data.users == min_no_of_users]
            threshold = pd.pivot_table(data_of_min_user[["metric", "item_name", "item_value"]], values="item_value", index=["item_name"], columns=["metric"])
            threshold = pd.DataFrame(threshold.to_records())
            threshold["threshold"] = threshold.art + 3 * threshold.sdrt
            threshold = threshold[["item_name", "threshold"]]

            # list_of_microservices = pd.unique(all_data.item_name)
            workloads = pd.pivot_table(all_data[all_data.users != min_no_of_users], values="item_value", index=["test_id", "test_set_id", "users", "item_name"], columns=["metric"], aggfunc=np.mean, fill_value=np.Infinity)
            workloads = pd.DataFrame(workloads.to_records())

            def verify_if_response_time_is_above_threshold(row):
                if threshold_metric == 1:
                    if np.max(threshold[threshold.item_name == row["item_name"]].threshold) > row["art"]:
                        return row["mix"]

                if threshold_metric == 2:
                    if np.max(threshold[threshold.item_name == row["item_name"]].threshold) > row["maxrt"]:
                        return row["mix"]

                return 0

            workloads["relative_mass"] = workloads.apply(verify_if_response_time_is_above_threshold, axis=1)
            workloads = workloads[["test_id", "test_set_id", "users", "relative_mass"]].groupby(by=["test_id", "test_set_id", "users"], as_index=False).sum()

            def calculate_absolute_mass(row):
                return row["relative_mass"] * np.max(binned_operational_profile[binned_operational_profile.workload == row["users"]].relative_frequency)

            workloads["absolute_mass"] = workloads.apply(calculate_absolute_mass, axis=1)
            workloads = workloads.sort_values(by=["test_set_id", "users"])

            test_sets = pd.read_sql(
                """SELECT id, name 
                FROM test_sets 
                WHERE project = :project""",
                connection,
                params=(project_id,)
            )


            domain_metric_per_test_set = workloads[["test_set_id", "absolute_mass"]].groupby(by=["test_set_id"], as_index=False).sum()
            domain_metric_per_test_set["test_set_name"] = domain_metric_per_test_set["test_set_id"].apply(lambda id: test_sets[test_sets.id == id].name.squeeze())
            domain_metric_per_test_set["absolute_mass"] = domain_metric_per_test_set["absolute_mass"].apply(lambda x: "{:.2f}".format(x))

            export_folder = os.path.abspath(os.path.join("./exported"))
            if not os.path.isdir(export_folder):
                logging.debug(f"Creating {export_folder}, since it does not exist.")
                os.makedirs(export_folder)

            export_results(export_folder, workloads, binned_operational_profile, test_sets, domain_metric_per_test_set)
            
            logging.info(f"Exported data to {export_folder}.")

def export_results(export_folder, workloads, binned_operational_profile, test_sets, domain_metric_per_test_set):
    data_to_export = workloads.drop(["test_id"], axis=1).rename(columns={"users": "x", "test_set_id": "group"})
    
    for _, row in test_sets.iterrows():
        data_to_export = data_to_export.replace(row["id"], row["name"])

    operational_profile_to_export = binned_operational_profile.rename(columns={"workload": "x", "relative_frequency": "y"})
    operational_profile_to_export["group"] = "operational_profile"

    data_to_export1 = data_to_export.drop(["relative_mass"], axis=1).rename(columns={ "absolute_mass": "y"})
    data_to_export1 = pd.concat([operational_profile_to_export, data_to_export1]).reset_index(drop=True)
    data_to_export1 = np.round(data_to_export1, decimals=3)
    data_to_export1 = data_to_export1.fillna(0).to_dict(orient="records")
    
    file_to_export = os.path.join(export_folder, "polygons.csv")
    with open(file_to_export, "w") as f:
        w = csv.DictWriter(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=["group", "x", "y"])
        w.writeheader()
        for row in data_to_export1:
            w.writerow(row)

    data_to_export2 = data_to_export.drop(["absolute_mass"], axis=1).rename(columns={ "relative_mass": "y"})
    data_to_export2 = np.round(data_to_export2, decimals=3)
    data_to_export2 = data_to_export2.fillna(0).to_dict(orient="records")    
    file_to_export = os.path.join(export_folder, "tests.csv")
    with open(file_to_export, "w") as f:
        w = csv.DictWriter(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=["group", "x", "y"])
        w.writeheader()
        for row in data_to_export2:
            w.writerow(row)

    data_to_export3 = domain_metric_per_test_set.drop(["test_set_id"], axis=1).loc[:, ["test_set_name", "absolute_mass"]].rename(columns={"test_set_name": "group"})
    data_to_export3 = np.round(data_to_export3, decimals=3)
    data_to_export3 = data_to_export3.fillna(0).to_dict(orient="records")
    
    file_to_export = os.path.join(export_folder, "domain_metric.csv")
    with open(file_to_export, "w") as f:
        w = csv.DictWriter(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=["group", "absolute_mass"])
        w.writeheader()
        for row in data_to_export3:
            w.writerow(row)
            

def get_predifined_operational_profile(operational_profile, all_data, workloads):
    # scale users in operational profile to users in tests
    max_no_of_users = np.max(all_data.users)

    max_no_of_requests = np.max(operational_profile.users)
    scale_factor = max_no_of_users / max_no_of_requests
    scaled_user_load = np.floor(operational_profile.users * scale_factor)
    scaled_operational_profile = pd.DataFrame({"users": scaled_user_load, "frequency": operational_profile.frequency})

    # calculate the relative frequencies in the operational profile
    total_number_of_accesses = np.sum(operational_profile.frequency)

    def calculate_frequency(x):
        return x / total_number_of_accesses

    scaled_operational_profile["relative_frequency"] = scaled_operational_profile["frequency"].apply(calculate_frequency)

    # calculate bins and sum relative frequencies for each bin
    scaled_operational_profile = insert_zero_users_record_at_the_beginning(scaled_operational_profile)

    # assign a fixed number of bins, this is Barbara's technique in the R script
    # number_of_bins = 10
    # scaled_operational_profile["workload_range"] = pd.cut(scaled_operational_profile.users, number_of_bins)
    # scaled_operational_profile["workload"] = scaled_operational_profile["workload_range"].apply(lambda range: int(range.right))

    # assign bins according to the present tests

    def assign_test(users):
        for x in workloads:
            if x >= users:
                return x

        return max(workloads)

    scaled_operational_profile["workload"] = scaled_operational_profile["users"].apply(assign_test)
    bins = scaled_operational_profile[["workload", "relative_frequency"]].groupby(by=["workload"], as_index=False).sum()
    return bins

def get_poisson_operational_profile(workloads, arrival_rate_per_second, time_in_seconds, steps):
    average_no_of_users = arrival_rate_per_second * time_in_seconds

    frequencies = []
    for i in range(len(workloads)):
        if i == 0:
            frequencies.append(poisson.cdf(workloads[i], average_no_of_users))
        else:
            frequencies.append(poisson.cdf(workloads[i], average_no_of_users) - poisson.cdf(workloads[i - 1], average_no_of_users))

    bins = pd.DataFrame({"workload": workloads, "relative_frequency": frequencies})
                
    return bins

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("project", help="Name of the project to analyze")
    parser.add_argument("--threshold", help="Use average (1) or maximum (2) response time", type=int, choices=range(1, 3), default=1)
    parser.add_argument("--profile", help="Use poisson (1) or predefined (2) operational profile", type=int, choices=range(1, 3), default=1)
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    create_dashboard(args.project, args.threshold, args.profile)
