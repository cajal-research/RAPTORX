import pickle

from openai_setup import setup_openai_key


def main():
    setup_openai_key()
    config = RetrievalAugmentationConfig()
    retrieval_augmentation = RetrievalAugmentation(config=config)

    with open('../demo/sample.txt', 'r') as file:
        docs = file.read()

    retrieval_augmentation.add_documents(docs)

    tree = retrieval_augmentation.tree
    file_path = '../demo/tree.pkl'
    with open(file_path, 'wb') as file:
        pickle.dump(tree, file)


if __name__ == '__main__':
    main()
