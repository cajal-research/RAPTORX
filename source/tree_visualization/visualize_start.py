import pickle
from pathlib import Path
from typing import List

from source.paths.path_reference import get_tree_pkl_path
from source.raptor.tree_structures import Node, Tree
from source.tree_visualization.visualize_core import TreeVisualizer


def load_tree(path):
    """Load the tree from a pickled file."""
    with open(path, "rb") as file:
        tree_object = pickle.load(file)
    return tree_object


def main():
    pkl_path = get_tree_pkl_path()
    tree = load_tree(pkl_path)
    root_node = Node(
        text="Root Node",  # You can replace this with an appropriate text for the root node
        index=-1,
        children=list(map(lambda x: x.index, tree.root_nodes.values())),
        embeddings=[]
    )
    # visualize_tree_graph(tree, special_nodes=[-1, 37, 9])
    visualizer = TreeVisualizer(root_node, tree, full_path_trail=[-1, 37, 9])
    visualizer.plot_tree(jupyter=False)


if __name__ == '__main__':
    main()
