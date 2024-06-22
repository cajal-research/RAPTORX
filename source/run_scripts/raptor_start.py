import pickle

from source.paths.path_reference import get_cinderella_folder_path
from source.raptor.RetrievalAugmentation import RetrievalAugmentationConfig, RetrievalAugmentation
from source.utils.openai_utils import setup_openai_api_key


def main():
    setup_openai_api_key()
    config = RetrievalAugmentationConfig()
    retrieval_augmentation = RetrievalAugmentation(config=config)

    with open(get_cinderella_folder_path() / 'cinderella_story.txt', 'r') as file:
        docs = file.read()

    retrieval_augmentation.add_documents(docs)

    tree = retrieval_augmentation.tree
    file_path = get_cinderella_folder_path() / 'tree.pkl'
    with open(file_path, 'wb') as file:
        pickle.dump(tree, file)


if __name__ == '__main__':
    main()
