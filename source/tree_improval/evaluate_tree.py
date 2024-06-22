import pandas as pd
from retriever import retrieve
from typing import List
from tqdm import tqdm

from source.models.tree_structures import Tree
from source.tree_improval.utils import get_path_to_leaf


def evaluate_tree(tree: Tree, dataset: pd.DataFrame) -> pd.DataFrame:
    shuffled_dataset = dataset.sample(frac=1).reset_index(drop=True)
    leaf_nodes = tree.leaf_nodes.keys()
    correct_path_dict = {leaf: get_path_to_leaf(tree, leaf) for leaf in leaf_nodes}

    questions = shuffled_dataset['question'].values.tolist()
    items = shuffled_dataset['node'].values.tolist()

    results = []

    for question, item in tqdm(zip(questions, items), total=len(questions), desc="Evaluating"):
        path, question_embedding = retrieve(question, tree)
        path_indexes = [node.index for node in path]
        correct_path = correct_path_dict[item]
        correct = (item == path[-1].index)

        result = {
            'question': question,
            'question_embedding': question_embedding,
            'retrieved_path': path_indexes,
            'correct_path': correct_path,
            'is_correct': correct
        }
        results.append(result)

    results_df = pd.DataFrame(results)
    accuracy = results_df['is_correct'].mean()
    print('Done!')
    print(f'Accuracy: {accuracy}')

    return results_df
