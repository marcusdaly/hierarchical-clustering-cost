import networkx as nx
import treelib as tl

import itertools

from typing import Callable, List, Tuple

import logging
from logging import debug

import sys
# debug(sys.getrecursionlimit())

# sys.setrecursionlimit(2000)

logging.basicConfig(level=logging.INFO)


def find_optimal(G: nx.Graph, cost: Callable[[nx.Graph, tl.Tree], float]) -> Tuple[List[tl.Tree], float]:
    remaining = list(G.nodes)
    all_trees = get_all_trees(remaining)
    costs = [(tree, cost(G, tree)) for tree in all_trees]
    minimum = min(costs, key=lambda x: x[1]) # TODO return all minimum trees.
    all_min_trees = [item[0] for item in costs if item[1] == minimum[1]]
    return all_min_trees, minimum[1]

def get_all_trees(remaining: List[int]) -> List[tl.Tree]:

    # initializations
    n = len(remaining)


    T = tl.Tree()
    T.create_node(-1, -1)

    currrent_parent = -1
    next_internal_node = -2

    all_trees = search_num_leaves(n, remaining, T, currrent_parent, next_internal_node)

    debug(f"We found {len(all_trees)} Trees!")

    # show all the trees (oh boy.)
    # for tree in all_trees:
    #     tree.show()

    return all_trees

def search_num_leaves(n_total: int, remaining: List[int], T: List[tl.Tree], currrent_parent: int, next_internal_node: int) -> List[tl.Tree]:
    debug(f"Enter search_num_leaves: {remaining} {currrent_parent} {next_internal_node}")
    all_trees = []

    # for each number of leaves...
    for num_leaves in range(0, len(remaining) + 1):
        # if no leaves, run with all internal
        if num_leaves == 0:
            # deep copy the tree for 0 leaves.
            t = tl.Tree(tree=T)

            all_trees.extend(search_num_internal_nodes(n_total, remaining, t, num_leaves, currrent_parent, next_internal_node))
        else:
            # for each combination of which leaves these are...
            for leaves in itertools.combinations(remaining, r=num_leaves):
                # deep copy the tree for this number and choice of leaves.
                t = tl.Tree(tree=T)

                # add the leaves
                for leaf in leaves:
                    t.create_node(leaf, leaf, parent=currrent_parent)

                # remaining leaves must be below some internal nodes.
                new_remaining = [r for r in remaining if r not in leaves]

                all_trees.extend(search_num_internal_nodes(n_total, new_remaining, t, num_leaves, currrent_parent, next_internal_node))

    debug(f"Exit search_num_leaves: {remaining} {currrent_parent} {next_internal_node}: {len(all_trees)}")
    return all_trees

def search_num_internal_nodes(
    n_total: int,
    remaining: List[int],
    T: List[tl.Tree],
    num_leaves: int,
    currrent_parent: int,
    next_internal_node: int,
) -> List[tl.Tree]:

    debug(f"Enter search_num_internal_nodes: {remaining} {num_leaves} {currrent_parent} {next_internal_node}")

    all_trees = []

    # if we didn't put any leaves at this level, we need more than one internal node.
    min_internal_nodes = 1 if num_leaves > 0 else 2

    # if no internal nodes, just return the tree.
    if len(remaining)+1 <= min_internal_nodes:
        debug(f"Exit search_num_internal_nodes Early!: {remaining} {num_leaves} {currrent_parent} {next_internal_node}: {len(all_trees)}")
        t = tl.Tree(tree=T)
        return [t]

    # for each number of internal nodes...
    for num_internal_nodes in range(min_internal_nodes, len(remaining)+1):
        # if we have more internal nodes than leaf nodes, we've done something wrong.
        if len(T.nodes) > 2 * n_total:
            continue

        # deep copy the tree for this number of internal nodes.
        t = tl.Tree(tree=T)

        internal_nodes = []

        this_next_internal_node = next_internal_node

        debug("creating")
        # t.show()
        for _ in range(num_internal_nodes):
            t.create_node(this_next_internal_node, this_next_internal_node, parent=currrent_parent)
            internal_nodes.append(this_next_internal_node)
            this_next_internal_node -= 1

        # note, this partitions the remaining data.
        partitions = algorithm_u(remaining, num_internal_nodes)

        # purge any partitions which have a segment with only 1 node in them.
        # these should've been leaves. (Note: this will allow recursion to terminate)
        partitions = [
            partition for partition in partitions if
            sum([int(len(segment) > 1) for segment in partition]) == len(partition)
        ]

        # t.show()
        all_trees.extend(search_all_partitions(n_total, remaining, t, internal_nodes, partitions, currrent_parent, this_next_internal_node))

    debug(f"Exit search_num_internal_nodes: {remaining} {num_leaves} {currrent_parent} {next_internal_node}: {len(all_trees)}")
    return all_trees

def search_all_partitions(
    n_total: int,
    remaining: List[int],
    T: tl.Tree,
    internal_nodes: List[int],
    partitions: List[List[List[int]]],
    currrent_parent: int,
    next_internal_node: int,
) -> List[tl.Tree]:

    debug(f"Enter search_all_partitions: {remaining} {internal_nodes} {currrent_parent} {next_internal_node}")

    all_trees = []

    # each internal node is now the root of a subtree. restart the search.
    for partition in partitions:
        t1 = tl.Tree(tree=T)

        # all the possible subtrees for each node
        node_subtrees = []

        for internal_node, segment in zip(internal_nodes, partition):
            node_subtrees.append(search_num_leaves(n_total, segment, t1.subtree(internal_node), internal_node, next_internal_node))
            next_internal_node -= len(segment) # may add a bunch of internal nodes!
            t1.remove_node(internal_node)

        # to get all possible trees resulting, use a cartesian product:
        all_node_subtree_combos = list(itertools.product(*node_subtrees))

        for node_subtree_combo in all_node_subtree_combos:
            # deep copy over this subtree combo for this partition of the data
            t2 = tl.Tree(tree=t1)



            # attach the subtrees below the parent.
            for subtree in node_subtree_combo:
                t2.paste(currrent_parent, subtree)

            all_trees.append(t2)

    debug(f"Exit search_all_partitions: {remaining} {internal_nodes} {currrent_parent} {next_internal_node}: {len(all_trees)}")
    return all_trees



# divide data into m (potentially unequal) partitions.
# Taken directly from https://codereview.stackexchange.com/questions/1526/finding-all-k-subset-partitions
def algorithm_u(ns: List[int], m: int) -> List[List[List[int]]]:
    debug(f"Enter algorithm_u: {ns} {m}")

    if m == 1:
        return [[ns]]

    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return list(f(m, n, 0, n, a))
