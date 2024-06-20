import pickle

from source.models.tree_structures import Node
from source.paths.path_reference import get_tree_pkl_path
from source.tree_visualization.visualize_core import visualize_tree_structure


def load_tree(path):
    """Load the tree from a pickled file."""
    with open(path, "rb") as file:
        tree_object = pickle.load(file)
    return tree_object


def visualize_tree_graph():
    # Load the tree from the pickled file
    file_path = get_tree_pkl_path()
    tree = load_tree(file_path)

    # Now create a new root Node on top of all root nodes
    root_node = Node(
        text="Root Node",  # You can replace this with an appropriate text for the root node
        index=-1,
        children=list(map(lambda x: x.index, tree.root_nodes.values())),
        embeddings=[]
    )

    visualize_tree_structure(root_node, tree)


def main():
    visualize_tree_graph()


if __name__ == '__main__':
    main()
