import ast
import json
from typing import Tuple

import pandas as pd

from source.datasets.dataset_utils import flatten_and_concat_dict
from source.paths.path_reference import get_crude_datasets_folder_path, get_datasets_folder_path


def load_qasper_dataset() -> Tuple[pd.DataFrame, pd.DataFrame]:
    qasper_folder_path = get_crude_datasets_folder_path()
    dev_file_path = qasper_folder_path / 'qasper_dev.json'
    train_file_path = qasper_folder_path / 'qasper_train.json'
    with open(dev_file_path, 'r') as f:
        dev_data = list(json.load(f).values())
    with open(train_file_path, 'r') as f:
        train_data = list(json.load(f).values())
    dev_dicts = [flatten_and_concat_dict(item) for item in dev_data]
    train_dicts = [flatten_and_concat_dict(item) for item in train_data]
    dev_df = pd.DataFrame(dev_dicts)
    train_df = pd.DataFrame(train_dicts)
    return dev_df, train_df


def load_narrative_qa_dataset() -> pd.DataFrame:
    narrative_qa_folder_path = get_crude_datasets_folder_path()
    narrative_qa_path = narrative_qa_folder_path / 'narrative_qa.csv'
    return pd.read_csv(narrative_qa_path)


def load_quality_dataset() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    quality_folder_path = get_crude_datasets_folder_path()
    dev_file_path = quality_folder_path / 'quality.dev'
    test_file_path = quality_folder_path / 'quality.test'
    train_file_path = quality_folder_path / 'quality.train'

    def load_and_parse_file(file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                json_dict = json.loads(stripped_line)
                data.append(json_dict)
        df = pd.DataFrame(data)
        return df

    dev_file_df = load_and_parse_file(dev_file_path)
    test_file_df = load_and_parse_file(test_file_path)
    train_file_df = load_and_parse_file(train_file_path)

    return dev_file_df, test_file_df, train_file_df


def save_to_csv(chunk_percentage: float = 0.1):
    qasper_dev, qasper_train = load_qasper_dataset()
    narrative_df = load_narrative_qa_dataset()
    quality_dev, quality_test, quality_train = load_quality_dataset()
    df_pool = {"qasper_dev": qasper_dev, "qasper_train": qasper_train, "narrative_qa": narrative_df,
               "quality_dev": quality_dev, "quality_test": quality_test, "quality_train": quality_train}
    for label, df in df_pool.items():
        sampled_df = df.sample(frac=chunk_percentage, random_state=1)
        csv_path = get_datasets_folder_path() / f"small_data/{label}.csv"
        sampled_df.to_csv(csv_path, index=False)
    return


def main():
    save_to_csv()


if __name__ == "__main__":
    main()
