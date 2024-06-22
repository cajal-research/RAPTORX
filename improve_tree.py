from tree_structures import Tree
import pandas as pd
import numpy as np
from retriever import retrieve
from typing import List
from tqdm import tqdm

LEARNING_RATE = 0.02

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

def improve_tree(tree: Tree, dataset: pd.DataFrame) -> pd.DataFrame:
    new_tree = tree
    all_nodes = tree.all_nodes
    shuffled_dataset = dataset.sample(frac=1).reset_index(drop=True)
    leaf_nodes = tree.leaf_nodes.keys()
    correct_path_dict = {leaf: get_path_to_leaf(tree, leaf) for leaf in leaf_nodes}
    questions = shuffled_dataset['question'].values.tolist()
    items = shuffled_dataset['node'].values.tolist()

    for question, item in tqdm(zip(questions, items), total=len(questions), desc="Improving tree"):
        path, query_embedding = retrieve(question, tree)
        correct_path = correct_path_dict[item]
        
        if item != path[-1].index:
            for i in range(len(path)):
                if correct_path[i] != path[i].index:
                    # Now update the tree from where the path diverged
                    # Enforce the correct path
                    vector = np.array(all_nodes[correct_path[i]].embeddings['OpenAI'])
                    new_embedding_1 = vector + LEARNING_RATE * (np.array(query_embedding) - vector)
                    new_tree = update_tree(new_tree, new_embedding_1, correct_path[i])
                    # Penalize the wrong path
                    new_embedding_2 = np.array(path[i].embeddings['OpenAI']) - LEARNING_RATE * (np.array(query_embedding) - path[i].embeddings['OpenAI'])
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
    