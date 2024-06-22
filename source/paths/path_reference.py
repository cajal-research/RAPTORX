from pathlib import Path


def get_root_folder_path():
    return Path(__file__).parent.parent


def get_datasets_folder_path():
    return Path(get_root_folder_path(), 'datasets')


def get_crude_datasets_folder_path():
    return Path(get_root_folder_path(), 'datasets/crude_data')


def get_normalized_datasets_folder_path():
    return Path(get_root_folder_path(), 'datasets/normalized_data')

def get_tree_pkl_path():
    return Path(get_root_folder_path(), 'models/tree.pkl')


def main():
    root_folder = get_root_folder_path()
    print(root_folder)
    return


if __name__ == '__main__':
    main()