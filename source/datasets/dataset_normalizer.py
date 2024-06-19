from pathlib import Path

import pandas as pd
import nltk
from sklearn.model_selection import train_test_split
from typing import Tuple, List

from path.path_reference import get_datasets_folder_path

# Ensure you have the necessary NLTK data files
nltk.download('punkt')


def tokenize_text(text: str) -> List[str]:
    """Tokenizes the input text into words."""
    return nltk.word_tokenize(text)


def preprocess_and_split(
        df: pd.DataFrame,
        text_column: str,
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Tokenizes text data and splits the dataset into training, validation, and test sets."""

    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame")

    # Handle missing values in the text column
    df[text_column] = df[text_column].fillna('')

    # Tokenize the text column
    df[text_column] = df[text_column].apply(tokenize_text)

    # Split the data into train and temp sets
    train_df, temp_df = train_test_split(df, test_size=test_size + val_size, random_state=random_state)

    # Calculate validation size as a proportion of the temp set
    val_relative_size = val_size / (test_size + val_size)

    # Split the temp set into validation and test sets
    val_df, test_df = train_test_split(temp_df, test_size=val_relative_size, random_state=random_state)

    return train_df, val_df, test_df



def save_datasets(train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame, dataset_name: str):
    """Saves the train, validation, and test sets to CSV files."""
    csv_path = get_datasets_folder_path() / "csvs"
    train_df.to_csv(Path(csv_path, f'{dataset_name}_val.csv'), index=False)
    val_df.to_csv(Path(csv_path, f'{dataset_name}_train.csv'), index=False)
    test_df.to_csv(Path(csv_path, f'{dataset_name}_test.csv'), index=False)


def preprocess_qasper():
    from dataset_loader import load_qasper_dataset
    qasper_dev, qasper_train = load_qasper_dataset()
    text_column = 'Paragraph'

    qasper_train_df, qasper_val_df, qasper_test_df = preprocess_and_split(qasper_train, text_column=text_column)
    save_datasets(qasper_train_df, qasper_val_df, qasper_test_df, 'qasper_train')

    qasper_dev_train_df, qasper_dev_val_df, qasper_dev_test_df = preprocess_and_split(qasper_dev,
                                                                                      text_column=text_column)
    save_datasets(qasper_dev_train_df, qasper_dev_val_df, qasper_dev_test_df, 'qasper_dev')


def preprocess_narrative_qa():
    from dataset_loader import load_narrative_qa_dataset
    narrative_df = load_narrative_qa_dataset()

    text_column = 'question'

    narrative_train_df, narrative_val_df, narrative_test_df = preprocess_and_split(narrative_df,
                                                                                   text_column=text_column)
    save_datasets(narrative_train_df, narrative_val_df, narrative_test_df, 'narrative_qa')


def preprocess_quality():
    from dataset_loader import load_quality_dataset
    quality_dev, quality_test, quality_train = load_quality_dataset()

    text_column = 'article'

    quality_train_df, quality_val_df, quality_test_df = preprocess_and_split(quality_train, text_column=text_column)
    save_datasets(quality_train_df, quality_val_df, quality_test_df, 'quality_train')

    quality_dev_train_df, quality_dev_val_df, quality_dev_test_df = preprocess_and_split(quality_dev,
                                                                                         text_column=text_column)
    save_datasets(quality_dev_train_df, quality_dev_val_df, quality_dev_test_df, 'quality_dev')

    quality_test_train_df, quality_test_val_df, quality_test_test_df = preprocess_and_split(quality_test,
                                                                                            text_column=text_column)
    save_datasets(quality_test_train_df, quality_test_val_df, quality_test_test_df, 'quality_test')


def main():
    preprocess_qasper()
    preprocess_narrative_qa()
    preprocess_quality()


if __name__ == "__main__":
    main()
