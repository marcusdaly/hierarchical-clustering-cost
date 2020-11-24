import treelib as tl
import networkx as nx

# note: currently unweighted.
def our_cost(G: nx.Graph, T: tl.Tree) -> float:
    cost = 0
    for edge in G.edges:
        lca = get_lca(T, edge[0], edge[1])
        subtree = T.subtree(lca)
        subtree_leaves = subtree.leaves()
        for leaf in subtree_leaves:
            cost += subtree.level(leaf.identifier)
    return cost

def get_lca(T: tl.Tree, x: int, y: int) -> int:
    # First, get to the same level
    while T.level(x) > T.level(y):
        x = T.parent(x).identifier
    while T.level(x) < T.level(y):
        y = T.parent(y).identifier

    # Then, increment both until it's the same node.
    while x != y:
        x = T.parent(x).identifier
        y = T.parent(y).identifier

    # now, this is the LCA.
    return x
