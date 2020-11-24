import networkx as nx
import treelib as tl

import itertools

from find_optimal import find_optimal, algorithm_u
from depth_cost import depth_cost
from dasgupta_cost import dasgupta_cost
from our_cost import our_cost

import sys

def main():
    # Get the cost of a couple trees.
    num_nodes = int(sys.argv[1])
    print(list(range(num_nodes)))
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    tree, cost = find_optimal(G, depth_cost)
    print(f"Min Cost Depth: {cost}")
    print("Tree:")
    tree.show()

    tree, cost = find_optimal(G, dasgupta_cost)
    print(f"Min Cost Dasgupta: {cost}")
    print("Tree:")
    tree.show()

    tree, cost = find_optimal(G, our_cost)
    print(f"Min Cost Us: {cost}")
    print("Tree:")
    tree.show()

    # From Dasgupta Paper
    num_nodes = int(sys.argv[1])
    print("From Dasgupta")
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (5, 6)])

    tree, cost = find_optimal(G, depth_cost)
    print(f"Min Cost Depth: {cost}")
    print("Tree:")
    tree.show()

    tree, cost = find_optimal(G, dasgupta_cost)
    print(f"Min Cost Dasgupta: {cost}")
    print("Tree:")
    tree.show()

    tree, cost = find_optimal(G, our_cost)
    print(f"Min Cost Us: {cost}")
    print("Tree:")
    tree.show()


if __name__ == '__main__':
    main()
