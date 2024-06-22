from openai import OpenAI
import numpy as np
from typing import List, Dict, Tuple

from raptor.tree_structures import Node, Tree


def embed(query: str) -> List[float]:
    """
    Embeds the query using a pre-trained model.
    """
    client = OpenAI()
    response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding


def cosine_similarity(embed1: List[float], embed2: List[float]) -> float:
    """
    Computes the cosine similarity between two embeddings.
    """
    return np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))


def best_match(query_embedding, nodes: Dict[int, Node]) -> Node:
    """
    Finds the best match for the query among the given nodes.
    """
    best_similarity = -1
    best_node = None
    for node in nodes.values():
        similarity = cosine_similarity(query_embedding, node.embeddings['OpenAI'])
        if similarity > best_similarity:
            best_similarity = similarity
            best_node = node
    return best_node


def retrieve(query: str, tree: Tree) -> Tuple[List[Node], List[float]]:
    """
    Retrieves the path in the tree that best matches the query.
    """

    all_nodes = tree.all_nodes
    query_embedding = embed(query)
    path = []

    previous_node = None
    for layer in range(tree.num_layers + 1):
        if layer == 0:
            previous_node = best_match(query_embedding, tree.root_nodes)
        else:
            children = {index: all_nodes[index] for index in previous_node.children}
            previous_node = best_match(query_embedding, children)
        path.append(previous_node)

    return path, query_embedding
