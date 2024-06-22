from tree_structures import Tree
from openai import OpenAI
import pandas as pd

DATA_PATH = 'data/syn_data/'


def synthesize(tree: Tree, file_name: str = 'dataset.csv', questions_per_chunk: int = 2) -> pd.DataFrame:
    """
    Synthesizes a dataset with questions for all the chunks (leaf_nodes)
    """
    chunks = tree.leaf_nodes
    data = {'node': [], 'question': []}

    for chunk in chunks:
        for _ in range(questions_per_chunk):
            question = generate_question(chunks[chunk].text)
            data['node'].append(chunk)
            data['question'].append(question)

    dataset = pd.DataFrame(data)
    dataset.to_csv(f'{DATA_PATH}{file_name}', index=False)
    return dataset


def generate_question(text: str) -> str:
    """
    Generates a question from a chunk of text using GPT-3.
    """
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Generate a question from the following text: " + text,
            }
        ],
        model="gpt-3.5-turbo",
    )
    question = chat_completion.choices[0].message.content

    return question
