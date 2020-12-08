import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from find_optimal import find_optimal
from find_approx import find_approx
from our_cost import our_cost

def compare_graph(graph_type: str, num_nodes: int, **kwargs):

    G = get_graph_by_type(graph_type=graph_type, num_nodes=num_nodes, **kwargs)

    trees, cost = find_optimal(G, our_cost)
    print(f"Min Cost Us: {cost}")
    print(f"Min Trees ({len(trees)})")
    for tree in trees:
        tree.show()

    tree, cost = find_approx(G)
    print(f"Min Cost Us: {cost}")
    print(f"Min Tree:")
    tree.show()

    print(G.nodes())

    labels = {n: n for n in G.nodes()}

    nx.draw(G, labels=labels)
    plt.show()

def compare_graphs(graph_type: str, num_nodes: int, **kwargs):
    num_graphs = 100

    optimal_costs = np.zeros((num_graphs,))
    approx_costs = np.zeros((num_graphs,))

    for i in range(num_graphs):

        G = get_graph_by_type(graph_type=graph_type, num_nodes=num_nodes, **kwargs)

        trees, cost = find_optimal(G, our_cost)
        print(f"Min Cost Us: {cost}")
        print(f"Min Trees ({len(trees)})")
        for tree in trees:
            tree.show()
        optimal_costs[i] = cost

        tree, cost = find_approx(G)
        print(f"Min Cost Us: {cost}")
        print(f"Min Tree:")
        tree.show()
        approx_costs[i] = cost

    diffs = approx_costs - optimal_costs
    mean_diff = np.mean(diffs)

    print(f"Optimal: {optimal_costs}")
    print(f"Approx: {approx_costs}")
    print(f"Difference: {diffs}")
    print(f"Mean Difference: {mean_diff}")

    unique, counts = np.unique(diffs, return_counts=True)
    norm_counts = counts / num_graphs
    percentile_90 = int(np.percentile(diffs, 90))
    max_diff = int(np.max(diffs))
    plt.bar(unique, norm_counts, width=0.9)
    plt.axvline(mean_diff, c="yellow", label=f"Mean ({mean_diff:.2})")
    plt.axvline(percentile_90, c="orange", label=f"90th Percentile ({percentile_90})")
    plt.axvline(max_diff, c="red", label=f"Max ({max_diff})")
    plt.xlabel("Difference from Optimal")
    plt.ylabel("Probability")
    plt.xlim(-0.5, np.max(diffs) + 0.5)
    plt.title(f"Difference from Optimal for {num_nodes}-node {graph_type} Graphs")
    plt.legend(loc="upper right")
    plt.show()

def get_graph_by_type(graph_type: str, num_nodes: int, **kwargs) -> nx.Graph:
    if graph_type == "E-R":
        return nx.erdos_renyi_graph(n=num_nodes, **kwargs)
    elif graph_type == "Random Tree":
        return nx.random_tree(n=num_nodes, **kwargs)
    elif graph_type == "r-ary":
        return nx.full_rary_tree(n=num_nodes, **kwargs)
    elif graph_type == "Planted Partition":
        return nx.planted_partition_graph(**kwargs)
