import networkx as nx
import treelib as tl
import numpy as np

def uid() -> int:
    return np.random.randint(np.iinfo(np.int32).min, -2)

def reset_ids(t: tl.Tree) -> tl.Tree:
    for node in t.all_nodes():
        if node.is_leaf():
            t.update_node(node.identifier, tag=node.tag, identifier=node.tag)
        else:
            t.update_node(node.identifier, identifier=uid())

    return t

# Creates a new root with the roots of t1 and t2 as the new root's children.
def join(t1: tl.Tree, t2: tl.Tree) -> tl.Tree:
    # work with copies.
    t1 = tl.Tree(tree=t1, deep=True)
    t2 = tl.Tree(tree=t2, deep=True)

    # reset all the identifiers:
    t1 = reset_ids(t1)
    t2 = reset_ids(t2)

    # Create the new tree.
    t_new = tl.Tree()
    r_new = uid()
    t_new.create_node(tag=-1, identifier=r_new)
    # combine into a tree
    t_new.paste(t_new.root, t1)
    t_new.paste(t_new.root, t2)

    return t_new

# t1 takes the root of t2 as one of its children.
def absorb(t1: tl.Tree, t2: tl.Tree) -> tl.Tree:
    # work with copies.
    t1 = tl.Tree(tree=t1, deep=True)
    t2 = tl.Tree(tree=t2, deep=True)

    # reset all the identifiers:
    t1 = reset_ids(t1)
    t2 = reset_ids(t2)

    t1.paste(t1.root, t2)

    return t1

# Makes the roots of t1 and t2 the same node.
def collapse(t1: tl.Tree, t2: tl.Tree) -> tl.Tree:
    # work with copies.
    t1 = tl.Tree(tree=t1, deep=True)
    t2 = tl.Tree(tree=t2, deep=True)

    # reset all the identifiers:
    t1 = reset_ids(t1)
    t2 = reset_ids(t2)

    # paste all the children of t2 into the root of t1
    for child in t2.children(t2.root):
        t1.paste(t1.root, t2.subtree(child.identifier))

    return t1

def share_any_edges(G: nx.Graph, t1: tl.Tree, t2: tl.Tree) -> bool:
    leaves1 = [t.tag for t in t1.leaves()]
    leaves2 = [t.tag for t in t2.leaves()]
    # if something in t1 has an edge to something in t2, return true
    for u, v in G.edges():
        if u in leaves1:
            if v in leaves2:
                return True
        if v in leaves1:
            if u in leaves2:
                return True
    # otherwise, return false.
    return False
