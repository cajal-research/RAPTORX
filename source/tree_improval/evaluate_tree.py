import pandas as pd

from raptor.tree_structures import Tree
from retriever import retrieve
from typing import List
from tqdm import tqdm

from source.tree_improval.utils import get_path_to_leaf, shuffle_and_prepare, get_correct_paths, \
    retrieve_path_and_embedding, create_result_entry


def evaluate_tree(tree: Tree, dataset: pd.DataFrame) -> pd.DataFrame:
    shuffled_dataset, questions, items = shuffle_and_prepare(dataset)
    correct_path_dict = get_correct_paths(tree)

    results = []

    for question, item in tqdm(zip(questions, items), total=len(questions), desc="Evaluating"):
        path, question_embedding = retrieve_path_and_embedding(question, tree)
        correct_path = correct_path_dict[item]
        result = create_result_entry(question, question_embedding, path, correct_path, item)
        results.append(result)

    results_df = pd.DataFrame(results)
    accuracy = results_df['is_correct'].mean()
    print('Done!')
    print(f'Accuracy: {accuracy}')

    return results_df