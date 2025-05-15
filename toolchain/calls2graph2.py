#!/usr/bin/env python3

import csv
import argparse
import logging
import random
import matplotlib.pyplot as plt
import networkx as nx
import fitz
import os
import json

from deap import base, creator, tools, algorithms

def compute_total_distance(G, node_order):
    node_index = {node: idx for idx, node in enumerate(node_order)}
    total_distance = 0
    for u, v in G.edges:
        distance = abs(node_index[u] - node_index[v])
        total_distance += distance
    return total_distance

def optimize_node_order(G, generations=50, population_size=100):
    nodes = list(G.nodes)
    num_nodes = len(nodes)

    # Create mapping
    idx_to_node = {i: node for i, node in enumerate(nodes)}

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(num_nodes), num_nodes)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval_individual(individual):
        ordered_nodes = [idx_to_node[i] for i in individual]
        return (compute_total_distance(G, ordered_nodes),)

    toolbox.register("evaluate", eval_individual)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=population_size)

    algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.2, ngen=generations, verbose=False)

    best_ind = tools.selBest(population, k=1)[0]
    best_node_order = [idx_to_node[i] for i in best_ind]
    return best_node_order


def save_dag_as_pdf(output_pdf, G, node_order_file=None, optimizeorder=False, width=0):
    if node_order_file:
        with open(node_order_file, 'r') as f:
            optimized_nodes = json.load(f)
        
        missing_nodes = [node for node in G.nodes if node not in optimized_nodes]
        if missing_nodes:
            optimized_nodes.extend(missing_nodes)
    elif optimizeorder:
        optimized_nodes = optimize_node_order(G)
    else:
        optimized_nodes = sorted(G.nodes)

    node_positions = {node: (i, 0) for i, node in enumerate(optimized_nodes)}

    in_degrees = [G.in_degree(node) for node in optimized_nodes]
    out_degrees = [G.out_degree(node) for node in optimized_nodes]
    max_in_degree = max(in_degrees) if in_degrees else 1
    max_out_degree = max(out_degrees) if out_degrees else 1

    def gray_to_red(val):
        return (0.5 + 0.5 * val, 0.5 * (1 - val), 0.5 * (1 - val))

    def gray_to_blue(val):
        return (0.5 * (1 - val), 0.5 * (1 - val), 0.5 + 0.5 * val)
    
    in_colors = [gray_to_blue(deg / max_in_degree) for deg in in_degrees]
    out_colors = [gray_to_red(deg / max_out_degree) for deg in out_degrees]

    fig, ax = plt.subplots(figsize=(width, 1.5))
    ax.set_axis_off()

    for node, (x, y), out_color, in_color in zip(optimized_nodes, node_positions.values(), out_colors, in_colors):
        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)

        ax.text(x, y + 0.04, node.lower(), ha='center', va='bottom', fontsize=7, rotation=-90)
        ax.plot(x, y, 'o', markersize=8, color=out_color)
        ax.text(x, y - 0.002, str(out_deg), ha='center', va='center', fontsize=5, color='white')
        ax.plot(x, y - 0.2, 'o', markersize=8, color=in_color)
        ax.text(x, y - 0.2 - 0.002, str(in_deg), ha='center', va='center', fontsize=5, color='white')

    for u, v in G.edges:
        x_start, y_start = node_positions[u]
        x_end, y_end = node_positions[v]
        ax.annotate("",
                    xy=(x_end, y_end - 0.2 + 0.015),
                    xytext=(x_start, y_start - 0.02),
                    arrowprops=dict(arrowstyle="->", color=(100/255, 100/255, 100/255), alpha=0.5)
)

    ax.set_ylim(-0.25, 0.2)
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.close()

def crop_pdf(input_pdf_path, output_pdf_path, left=0, bottom=0, right=0, top=0):
    doc = fitz.open(input_pdf_path)

    for page in doc:
        rect = page.rect  # original page rectangle
        # Define new rectangle with specified margins
        new_rect = fitz.Rect(
            rect.x0 + left, 
            rect.y0 + top,  
            rect.x1 - right,
            rect.y1 - bottom
        )
        page.set_cropbox(new_rect)

    doc.save(output_pdf_path)


def read_csv_and_build_graph(csv_filename):
    G = nx.DiGraph()

    with open(csv_filename, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            from_service = row['from']
            to_service = row['to']
            G.add_edge(from_service, to_service)

    return G

def main():
    parser = argparse.ArgumentParser(description="Generate a simple DAG PDF from a service call CSV file.")
    parser.add_argument("input_csv", help="Path to input CSV file.")
    parser.add_argument("output_pdf", help="Path to output PDF file.")
    parser.add_argument("--logging", type=int, choices=range(0, 6), default=2,
                        help="Logging level from 1 (everything) to 5 (nothing)")
    parser.add_argument("--cropleft", type=float, default=0, help="Crop margin from the left in points.")
    parser.add_argument("--cropbottom", type=float, default=0, help="Crop margin from the bottom in points.")
    parser.add_argument("--cropright", type=float, default=0, help="Crop margin from the right in points.")
    parser.add_argument("--croptop", type=float, default=0, help="Crop margin from the top in points.")
    parser.add_argument("--width", type=float, default=0, help="Width of the image.")
    parser.add_argument("--orderfile", type=str, default=None,
                        help="Path to a JSON file specifying node order (optional).")
    parser.add_argument("--optimizeorder", action="store_true",
                        help="Enable node order optimization with a genetic algorithm.")

    args = parser.parse_args()

    logging.basicConfig(format="%(message)s", level=args.logging * 10)

    G = read_csv_and_build_graph(args.input_csv)
    save_dag_as_pdf(args.output_pdf, G,
                    node_order_file=args.orderfile,
                    optimizeorder=args.optimizeorder,
                    width=args.width)

    base, ext = os.path.splitext(args.output_pdf)
    output_pdf_path = f"{base}_cropped{ext}"
    crop_pdf(args.output_pdf, output_pdf_path,
             left=args.cropleft, bottom=args.cropbottom,
             right=args.cropright, top=args.croptop)
    
    os.remove(args.output_pdf)    
    os.rename(output_pdf_path, args.output_pdf)

if __name__ == "__main__":
    main()
