import networkx as nx
import matplotlib.pyplot as plt

from itertools import count

from find_approx import find_approx

def plot_top_level():
    num_groups = 15
    per_group = 6
    G = nx.planted_partition_graph(l=num_groups, k=per_group, p_in=0.99, p_out=0.01)
    tree, cost = find_approx(G)
    print(f"Min Cost Us: {cost}")
    print(f"Min Tree:")
    tree.show()

    groups = []

    for child in tree.children(tree.root):
        group = []
        for leaf in tree.leaves():
            if tree.is_ancestor(child.identifier, leaf.identifier):
                group.append(leaf.identifier)
        groups.append(group)

    label_dict = {n: i for i, group in enumerate(groups) for n in group}

    nx.set_node_attributes(G, label_dict, "group")
    plt.figure(figsize=(14, 8))

    # coloring
    groups = set(nx.get_node_attributes(G,"group").values())
    mapping = dict(zip(sorted(groups),count()))
    nodes = G.nodes()
    node_colors = [mapping[G.nodes()[n]["group"]] for n in nodes]
    node_sizes = [14 for n in nodes]
    cmap = plt.cm.get_cmap('rainbow')


    nx.draw(G, node_color = node_colors, width=0.1, cmap = cmap, labels={i: i for i, _ in enumerate(G.nodes())})

    print(groups)
    plt.show()
