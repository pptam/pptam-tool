#!/usr/bin/env python3

import csv
import argparse
import logging
import os
import networkx as nx
import pygraphviz as pgv

def save_dag_as_pdf(output_pdf, G, hide_weights=True, layout='dot', sep=0.5, nodesep=0.5, ranksep=0.75):
    edges = [(u, v, G[u][v].get("weight", 1)) for u, v in G.edges]

    graph = pgv.AGraph(directed=True)
    graph.graph_attr.update(
        splines="true",
        overlap="false",
        sep=str(sep),
        nodesep=str(nodesep),
        ranksep=str(ranksep),
        concentrate="true", 
        pack="true",       
        packmode="clust"
    )

    for u, v, weight in edges:
        if hide_weights:
            graph.add_edge(u, v)
        else:
            graph.add_edge(u, v, label=weight)

    graph.layout(prog=layout)
    graph.draw(output_pdf)

def read_csv_and_build_graph(csv_filename):
    G = nx.DiGraph()

    with open(csv_filename, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            from_service = row['from']
            to_service = row['to']
            G.add_edge(from_service, to_service)

    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a DAG PDF from a service call CSV file.")
    parser.add_argument("input_csv", help="Path to input CSV file.")
    parser.add_argument("output_pdf", help="Path to output PDF file.")
    parser.add_argument("--hide_weights", type=bool, default=True, help="Hide weights on edges (default: True)")
    parser.add_argument("--layout", type=str, default="dot", help="Graph layout engine (dot, neato, circo, twopi, fdp, etc.). Default is dot.")
    parser.add_argument("--sep", type=float, default=0.5, help="Minimum separation between clusters (default: 0.5)")
    parser.add_argument("--nodesep", type=float, default=0.5, help="Minimum separation between nodes (default: 0.5)")
    parser.add_argument("--ranksep", type=float, default=0.75, help="Vertical separation between ranks (default: 0.75)")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    G = read_csv_and_build_graph(args.input_csv)

    save_dag_as_pdf(
        args.output_pdf,
        G,
        hide_weights=args.hide_weights,
        layout=args.layout,
        sep=args.sep,
        nodesep=args.nodesep,
        ranksep=args.ranksep
    )