import networkx as nx
import treelib as tl
import numpy as np
import matplotlib.pyplot as plt

import itertools

from find_optimal import find_optimal, algorithm_u
from find_approx import find_approx
from depth_cost import depth_cost
from dasgupta_cost import dasgupta_cost
from our_cost import our_cost
from optimality_comparison import compare_graph, compare_graphs, compare_graph_means
from plot_partitions import plot_top_level

import sys

def main():
    # Get the cost of a couple trees.

    # First, look at a clique.
    # num_nodes = int(sys.argv[1])
    # G = nx.Graph()
    # G.add_nodes_from(range(1, num_nodes+1))
    # for i in range(1, num_nodes+1):
    #     for j in range(i+1, num_nodes+1):
    #         G.add_edge(i, j)

    # Here, Look at 2 3-cliques connected by an edge.
    # num_nodes = 6
    # G = nx.Graph()
    # G.add_nodes_from(range(1, num_nodes+1))
    # for i in range(1, 4):
    #     for j in range(i+1, 4):
    #         G.add_edge(i, j)
    # for i in range(4, 7):
    #     for j in range(i+1, 7):
    #         G.add_edge(i, j)
    # G.add_edge(1, 4)
    # trees, cost = find_optimal(G, depth_cost)
    # print(f"Min Cost Depth: {cost}")
    # print(f"Min Trees ({len(trees)})")
    # for tree in trees:
    #     tree.show()
    #
    # trees, cost = find_optimal(G, dasgupta_cost)
    # print(f"Min Cost Dasgupta: {cost}")
    # print(f"Min Trees ({len(trees)})")
    # for tree in trees:
    #     tree.show()

    # trees, cost = find_optimal(G, our_cost)
    # print(f"Min Cost Us: {cost}")
    # print(f"Min Trees ({len(trees)})")
    # for tree in trees:
    #     tree.show()
    #
    # tree, cost = find_approx(G)
    # print(f"Min Cost Us: {cost}")
    # print(f"Min Tree:")
    # tree.show()

    # From Dasgupta Paper
    # num_nodes = 6
    # print("From Dasgupta")
    # G = nx.Graph()
    # G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (5, 6)])

    # trees, cost = find_optimal(G, depth_cost)
    # print(f"Min Cost Depth: {cost}")
    # print(f"Min Trees ({len(trees)})")
    # for tree in trees:
    #     tree.show()
    #
    # trees, cost = find_optimal(G, dasgupta_cost)
    # print(f"Min Cost Dasgupta: {cost}")
    # print(f"Min Trees ({len(trees)})")
    # for tree in trees:
    #     tree.show()

    # trees, cost = find_optimal(G, our_cost)
    # print(f"Min Cost Us: {cost}")
    # print(f"Min Trees ({len(trees)})")
    # for tree in trees:
    #     tree.show()
    #

    # plot_top_level()

    # costs = np.random.random((3, 3, 5))
    # # length of costs array currently.
    # c = costs.shape[0]
    #
    # # add absurdly high cost to upper diagonal to not consider these.
    # costs = costs + (1e15 * np.triu(np.ones((c, c)))).reshape((c, c, 1))
    #
    # print(costs)
    #
    # # find cost-minimizing pair and merge type
    # min_pair_index_flat = np.argmin(costs) # This gives index of flattened.
    #
    # # recover indices.
    # i_min = min_pair_index_flat // costs.shape[2] // c
    # j_min = min_pair_index_flat // costs.shape[2] % c
    # k_min = min_pair_index_flat % costs.shape[2]
    #
    # print(f"min: {i_min}, {j_min}, {k_min} = {costs[i_min,j_min,k_min]}")

    # num_groups = 2
    # per_group = 3
    # num_nodes = 6
    # compare_graphs(graph_type="Planted Partition", num_nodes=num_nodes, l=num_groups, k=per_group, p_in=0.9, p_out=0.3)
    # # compare_graphs(graph_type="E-R", num_nodes=num_nodes, p=0.5)
    # # compare_graphs(graph_type="Random Tree", num_nodes=num_nodes)
    # # compare_graph(graph_type="Line", num_nodes=num_nodes)
    node_range = [2, 3, 4, 5, 6, 7]
    # compare_graph_means(graph_type="Barabási–Albert", node_range=node_range, m=1)
    compare_graph_means(graph_type="E-R", node_range=node_range, p=0.3)
    # compare_tree()


if __name__ == '__main__':
    main()
