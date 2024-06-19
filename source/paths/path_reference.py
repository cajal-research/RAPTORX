from pathlib import Path


def get_root_folder_path():
    return Path(__file__).parent.parent


def get_crude_datasets_folder_path():
    return Path(get_root_folder_path(), 'datasets/crude_data')


def get_normalized_datasets_folder_path():
    return Path(get_root_folder_path(), 'datasets/normalized_data')


def main():
    root_folder = get_root_folder_path()
    print(root_folder)


if __name__ == '__main__':
    main()
