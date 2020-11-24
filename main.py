import networkx as nx
import treelib as tl

import itertools

from find_optimal import find_optimal, algorithm_u

def main():
    # Get the cost of a couple trees.
    # print(algorithm_u([0, 1, 2, 3], 1))
    # print("[0, 1]:")
    # G = nx.Graph()
    # G.add_nodes_from([0, 1])
    # print(len(find_optimal(G, None)))
    #
    # print("[0, 1, 2]:")
    # G = nx.Graph()
    # G.add_nodes_from([0, 1, 2])
    # print(len(find_optimal(G, None)))
    #
    # print("[0, 1, 2, 3]:")
    # G = nx.Graph()
    # G.add_nodes_from([0, 1, 2, 3])
    # print(len(find_optimal(G, None)))
    #
    # print("[0, 1, 2, 3, 4]:")
    # G = nx.Graph()
    # G.add_nodes_from([0, 1, 2, 3, 4])
    # print(len(find_optimal(G, None)))

    # print("[0, 1, 2, 3, 4, 5]:")
    # G = nx.Graph()
    # G.add_nodes_from([0, 1, 2, 3, 4, 5])
    # print(len(find_optimal(G, None)))

    print("[0, 1, 2, 3, 4, 5, 6]:")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
    print(len(find_optimal(G, None)))


    # G = nx.Graph()
    # G.add_nodes_from([0, 1, 2, 3, 4])
    #
    # find_optimal(G, None)
    # print("hi")


if __name__ == '__main__':
    main()
