from typing import Callable, List, Tuple

import networkx as nx
import treelib as tl
import numpy as np

from our_cost import our_cost
from utils import join, absorb, collapse, uid, share_any_edges

# implements the approximate agglomerative algorithm using our cost.
def find_approx(G: nx.Graph) -> Tuple[tl.Tree, float]:
    n = len(G.nodes())
    # Initialize C
    C = []
    for v in G.nodes():
        # create a tree with a single root and a leaf.
        T = tl.Tree()
        root = uid()
        T.create_node(-1, root)
        T.create_node(v, v, parent=root)
        C.append(T)

    # fill out the initial costs (lower diagonal only). (4 for each pair)
    costs = np.zeros((n, n, 4)) # len(C) (tree 1) x len(C) (tree 2) x 4 (merged tree)
    for j in range(n):
        for k in range(j):
            # only consider a merge if that pair would add an edge to the graph.
            # otherwise, it is an uninformative merge.
            if share_any_edges(G, C[j], C[k]):

                # join and collapse are symmetric.
                join_cost = our_cost(G, join(C[j], C[k]))
                collapse_cost = our_cost(G, collapse(C[j], C[k]))

                # b/c absorb is asymmetric, must do both ways for absorb.
                absorb_into_j_cost = our_cost(G, absorb(C[j], C[k]))
                absorb_into_k_cost = our_cost(G, absorb(C[k], C[j]))

                costs[j, k, 0] = join_cost
                costs[j, k, 1] = collapse_cost
                costs[j, k, 2] = absorb_into_j_cost
                costs[j, k, 3] = absorb_into_k_cost
            # if dont share an edge, don't consider the pair.
            else:
                costs[j, k, 0] = 1e15
                costs[j, k, 1] = 1e15
                costs[j, k, 2] = 1e15
                costs[j, k, 3] = 1e15

    # Main Loop.
    for i in range(1, n):
        # debug the trees at this step:
        print(f"Step {i}")
        for tree in C:
            print(tree)

        # length of costs array currently.
        c_len = costs.shape[0]

        # add absurdly high cost to upper diagonal to not consider these.
        costs = costs + (1e20 * np.triu(np.ones((c_len, c_len)))).reshape((c_len, c_len, 1))

        # find cost-minimizing pair and merge type
        min_pair_index_flat = np.argmin(costs) # This gives index of flattened.

        # recover indices.
        j_min = min_pair_index_flat // costs.shape[2] // c_len
        k_min = min_pair_index_flat // costs.shape[2] % c_len
        l_min = min_pair_index_flat % costs.shape[2]

        # print(f"min: {j_min}, {k_min}, {l_min} = {costs[j_min,k_min,l_min]}")

        # get the resulting minimizing tree.
        if l_min == 0:
            new_tree = join(C[j_min], C[k_min])
        elif l_min == 1:
            new_tree = collapse(C[j_min], C[k_min])
        elif l_min == 2:
            new_tree = absorb(C[j_min], C[k_min])
        else:
            new_tree = absorb(C[k_min], C[j_min])

        # get the new set of trees
        C = [tree for ti, tree in enumerate(C) if ti not in [j_min, k_min]]
        C.append(new_tree)

        # recalculate the new costs (again, only need lower diagonal)


        # add in new row
        costs = np.append(costs, np.zeros((1, costs.shape[1], costs.shape[2])), axis=0)
        costs = np.append(costs, np.zeros((costs.shape[0], 1, costs.shape[2])), axis=1)

        # get rid of old rows.
        costs = np.delete(costs, (j_min, k_min), axis=0)
        costs = np.delete(costs, (j_min, k_min), axis=1)

        # fill in new row
        j = -1
        for k in range(costs.shape[1]-1):
            if share_any_edges(G, C[j], C[k]):
                join_cost = our_cost(G, join(C[j], C[k]))
                collapse_cost = our_cost(G, collapse(C[j], C[k]))

                # b/c absorb is asymmetric, must do both ways for absorb.
                absorb_into_j_cost = our_cost(G, absorb(C[j], C[k]))
                absorb_into_k_cost = our_cost(G, absorb(C[k], C[j]))

                costs[j, k, 0] = join_cost
                costs[j, k, 1] = collapse_cost
                costs[j, k, 2] = absorb_into_j_cost
                costs[j, k, 3] = absorb_into_k_cost
            else:
                costs[j, k, 0] = 1e15
                costs[j, k, 1] = 1e15
                costs[j, k, 2] = 1e15
                costs[j, k, 3] = 1e15

        print(f"min k: {l_min}")

    assert len(C) == 1
    return C[0], our_cost(G, C[0])
