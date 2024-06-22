import pandas as pd
import numpy as np

from raptor.tree_structures import Tree
from retriever import retrieve
from typing import List
from tqdm import tqdm
from source.tree_improval.utils import get_path_to_leaf, shuffle_and_prepare, get_correct_paths, \
    retrieve_path_and_embedding

LEARNING_RATE = 0.02


def improve_tree(tree: Tree, dataset: pd.DataFrame) -> pd.DataFrame:
    shuffled_dataset, questions, items = shuffle_and_prepare(dataset)
    correct_path_dict = get_correct_paths(tree)
    new_tree = tree
    all_nodes = tree.all_nodes

    for question, item in tqdm(zip(questions, items), total=len(questions), desc="Improving tree"):
        path, query_embedding = retrieve_path_and_embedding(question, tree)
        correct_path = correct_path_dict[item]

        if item != path[-1].index:
            for i in range(len(path)):
                if correct_path[i] != path[i].index:
                    # Update the tree from where the path diverged
                    vector = np.array(all_nodes[correct_path[i]].embeddings['OpenAI'])
                    new_embedding_1 = vector + LEARNING_RATE * (np.array(query_embedding) - vector)
                    new_tree = update_tree(new_tree, new_embedding_1, correct_path[i])
                    # Penalize the wrong path
                    new_embedding_2 = np.array(path[i].embeddings['OpenAI']) - LEARNING_RATE * (
                                np.array(query_embedding) - path[i].embeddings['OpenAI'])
                    new_tree = update_tree(new_tree, new_embedding_2, path[i].index)
                    break

    return new_tree


def update_tree(tree: Tree, new_embedding: List[float], index: int) -> Tree:
    tree.all_nodes[index].embeddings['OpenAI'] = new_embedding
    for idx in tree.layer_to_nodes:
        for node_list_idx, node in enumerate(tree.layer_to_nodes[idx]):
            if node.index == index:
                tree.layer_to_nodes[idx][node_list_idx].embeddings['OpenAI'] = new_embedding
    if index in tree.leaf_nodes.keys():
        tree.leaf_nodes[index].embeddings['OpenAI'] = new_embedding
    if index in tree.root_nodes.keys():
        tree.root_nodes[index].embeddings['OpenAI'] = new_embedding
    return tree
