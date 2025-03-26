import logging
import requests
import networkx as nx
import json
import os
import pandas as pd
from datetime import datetime, timedelta, timezone
import pygraphviz as pgv

def fetch_services(jaeger_api_url):
    response = requests.get(f"{jaeger_api_url}/services")
    response.raise_for_status()
    return response.json().get("data", [])


def fetch_dependencies(jaeger_api_url):
    response = requests.get(f"{jaeger_api_url}/dependencies")
    response.raise_for_status()
    return response.json()


def to_rfc3339nano(dt):
    return dt.isoformat(timespec='microseconds').replace("+00:00", "Z")

def fetch_traces(jaeger_api_url, service_name, last_seconds=600):
    end_dt = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    start_dt = end_dt - timedelta(seconds=last_seconds) + timedelta(hours=1)

    print(start_dt)
    print(end_dt)

    params = {
        "query.start_time_min": to_rfc3339nano(start_dt),
        "query.start_time_max": to_rfc3339nano(end_dt),
        "limit": 1000000
    }
    response = requests.get(f"{jaeger_api_url}/v1/traces", params=params)
    response.raise_for_status()
    return response.json()


def build_dag(dependencies_data):
    G = nx.DiGraph()
    
    if "data" not in dependencies_data:
        return G

    for entry in dependencies_data["data"]:
        parent = entry["parent"]
        child = entry["child"]
        G.add_edge(parent, child, weight=entry.get("callCount", 1))
    
    return G


def save_dag_as_json(output, G):
    dag_data = nx.node_link_data(G, edges="edges")
    file_to_write = os.path.join(output, "dag.json")
    with open(file_to_write, "w") as f:
        json.dump(dag_data, f, indent=4)


def save_dag_as_csv(output, G):
    file_to_write = os.path.join(output, "dag.csv")
    edges = [(u, v, G[u][v].get("weight", 1)) for u, v in G.edges]
    df = pd.DataFrame(edges, columns=["Parent", "Child", "Weight"])
    df.to_csv(file_to_write, index=False)


def save_dag_as_pdf(output, G):
    edges = [(u, v, G[u][v].get("weight", 1)) for u, v in G.edges]
    df = pd.DataFrame(edges, columns=["Parent", "Child", "Weight"])

    graph = pgv.AGraph(directed=True)
    for _, row in df.iterrows():
        graph.add_edge(row['Parent'], row['Child'], label=row['Weight'])
    
    graph.layout(prog='dot')  # Use dot layout for hierarchy
    file_to_write = os.path.join(output, "dag.pdf")
    graph.draw(file_to_write)

def after(current_configuration, design_path, output, test_id):
    jaeger_api_url = current_configuration["jaeger_api_url"]
    seconds_to_wait_before_after = int(current_configuration["seconds_to_wait_before_after"])
    run_time_in_seconds = int(current_configuration["run_time_in_seconds"])
    run_time = run_time_in_seconds + seconds_to_wait_before_after

    try:
        trace_data = fetch_traces(jaeger_api_url, None, run_time)
        file_to_write = os.path.join(output, f"traces.json")
        with open(file_to_write, "w") as f:
            json.dump(trace_data, f, indent=4)

        # services = fetch_services(jaeger_api_url)
        
        # for service in services:
        #     try:
        #         trace_data = fetch_traces(jaeger_api_url, service, run_time)
        #         if trace_data and "data" in trace_data:
        #             file_to_write = os.path.join(output, f"traces_{service}.json")
        #             with open(file_to_write, "w") as f:
        #                 json.dump(trace_data, f, indent=4)
        #     except requests.exceptions.RequestException as e:
        #         logging.error(f"Error fetching traces for service {service}: {e}")
                
        # dependencies_data = fetch_dependencies(jaeger_api_url)
        # dag = build_dag(dependencies_data)
        # save_dag_as_json(output, dag)
        # save_dag_as_csv(output, dag)
        # save_dag_as_pdf(output, dag)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from Jaeger: {e}")

    