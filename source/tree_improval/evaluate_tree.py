import pandas as pd

from tqdm import tqdm

from source.paths.path_reference import get_tree_pkl_path, get_syn_dataset_path
from source.raptor.tree_structures import Tree
from source.tree_improval.utils import get_path_to_leaf, shuffle_and_prepare, get_correct_paths, \
    retrieve_path_and_embedding, create_result_entry
from source.tree_visualization.visualize_start import load_tree
from source.utils.openai_utils import setup_openai_api_key


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


def main():
    setup_openai_api_key()
    pkl_path = get_tree_pkl_path()
    tree = load_tree(pkl_path)
    dataset_path = get_syn_dataset_path()
    dataset = pd.read_csv(dataset_path)
    evaluate_tree(tree, dataset)


if __name__ == '__main__':
    main()
