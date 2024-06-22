from typing import Tuple, Dict, List
from retriever import retrieve
import pandas as pd

from source.models.tree_structures import Tree


def get_path_to_leaf(tree: Tree, leaf_node_index: str) -> List[int]:
    layers = tree.layer_to_nodes
    current_node = leaf_node_index
    path = list([current_node])
    for idx, layer in layers.items():
        if idx == 0:
            continue
        for node in layer:
            if current_node in node.children:
                current_node = node.index
                path.append(current_node)
                break
    return path[::-1]


def shuffle_and_prepare(dataset):
    shuffled_dataset = dataset.sample(frac=1).reset_index(drop=True)
    questions = shuffled_dataset['question'].values.tolist()
    items = shuffled_dataset['node'].values.tolist()
    return shuffled_dataset, questions, items


def get_correct_paths(tree):
    leaf_nodes = tree.leaf_nodes.keys()
    correct_path_dict = {leaf: get_path_to_leaf(tree, leaf) for leaf in leaf_nodes}
    return correct_path_dict


def retrieve_path_and_embedding(question, tree):
    return retrieve(question, tree)


def create_result_entry(question, question_embedding, path, correct_path, item):
    return {
        'question': question,
        'question_embedding': question_embedding,
        'retrieved_path': [node.index for node in path],
        'correct_path': correct_path,
        'is_correct': (item == path[-1].index)
    }
