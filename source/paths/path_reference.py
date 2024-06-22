from pathlib import Path


def get_root_folder_path():
    return Path(__file__).parent.parent


def get_data_folder_path():
    return Path(get_root_folder_path(), 'data')


def get_datasets_folder_path():
    return Path(get_root_folder_path(), 'datasets')


def get_crude_datasets_folder_path():
    return Path(get_root_folder_path(), 'datasets/crude_data')


def get_normalized_datasets_folder_path():
    return Path(get_root_folder_path(), 'datasets/normalized_data')


def get_tree_pkl_path():
    return Path(get_root_folder_path(), 'data/tree.pkl')


def get_syn_dataset_path():
    return Path(get_data_folder_path(), 'syn_data/dataset.csv')


def main():
    root_folder = get_tree_pkl_path()
    print(root_folder)
    return


if __name__ == '__main__':
    main()
