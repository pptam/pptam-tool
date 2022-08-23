#!/usr/bin/env python3

import os
import argparse
import logging
import contextlib
import sqlite3
from datetime import datetime
import csv
import uuid

def extract(file_name, constraint):
    statement = f"""
select * from (select
	distinct
	service_id, 
	service, 
	timestamp,
	SUM(r.value) filter (where r.metric=6) over (partition by service_id,tp.name) as response_time_max,
	SUM(r.value) filter (where r.metric=1) over (partition by service_id,tp.name) as requests,
	SUM(tp.value) filter (where tp.name ='docker_memory_limit_in_megabytes') over (partition by service_id,metric) as docker_memory_limit_in_megabytes,
	SUM(tp.value) filter (where tp.name ='docker_memory_limit_in_megabytes_of_databases') over (partition by service_id,metric) as docker_memory_limit_in_megabytes_of_databases,
	SUM(tp.value) filter (where tp.name ='docker_java_memory_limit_in_megabytes') over (partition by service_id,metric) as docker_java_memory_limit_in_megabytes,
	SUM(tp.value) filter (where tp.name ='load') over (partition by service_id,metric) as load
    from (
		select 
			id as service_id, 
			substr(i.name, 1, instr(i.name, '@') - 1) AS service, 
			substr(i.name, instr(i.name, '@') + 1) AS timestamp
		from items i 
		) items inner join results r on items.service_id  = r.item  inner join test_properties tp on r.test = tp.test
where service not like '%_spawning' and service not like 'admin_%' and metric in (1,6) and tp.name in ('load', 'docker_memory_limit_in_megabytes', 'docker_memory_limit_in_megabytes_of_databases', 'docker_java_memory_limit_in_megabytes')
order by service, timestamp
) where docker_java_memory_limit_in_megabytes={constraint}
    """
    
    export_folder = os.path.abspath(os.path.join("./exported"))
    if not os.path.isdir(export_folder):
        logging.debug(f"Creating {export_folder}, since it does not exist.")
        os.makedirs(export_folder)

    fieldnames = ["instance","counter_name","timestamp","response_time","response_time_max","response_time_min","requests","cpu_utilization_latest","cpu_utilization_max","cpu_utilization_min","ram_utilization_latest","ram_utilization_max","ram_utilization_min","load","provider"]

    parameters = ()
    with contextlib.closing(sqlite3.connect("pptam.db")) as connection:
        with connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute(statement, parameters)
                data_to_export = cursor.fetchall()

                file_to_export = os.path.join(export_folder, f"{file_name}-{constraint}.csv")
                with open(file_to_export, "w") as f:
                    w = csv.DictWriter(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
                    w.writeheader()
                    for row in data_to_export:
                        row_to_export = {}
                        row_to_export["instance"] = "trainticket"
                        row_to_export["counter_name"] = row[1]
                        row_to_export["timestamp"] = datetime.fromtimestamp(int(row[2])).strftime("%Y-%m-%d %H:%M:%S")
                        row_to_export["response_time_max"] = row[3]
                        row_to_export["requests"] = int(row[4])
                        row_to_export["load"] = row[8]
                        w.writerow(row_to_export)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a dataset consisting of different metrics.")
    parser.add_argument("name", help="Name of the file")
    parser.add_argument("constraint", help="Value of the constraint")
    parser.add_argument("--logging", help="Logging level from 1 (everything) to 5 (nothing)", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    extract(args.name, args.constraint)