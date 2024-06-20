import csv
import json

from source.paths.path_reference import get_datasets_folder_path

CRUDE_DATA_FOLDER = get_datasets_folder_path() / 'crude_data'
NORMALIZED_DATA_FOLDER = get_datasets_folder_path() / 'normalized_data'


def save_to_csv(standardized_data, output_file):
    output_path = NORMALIZED_DATA_FOLDER / output_file
    fieldnames = ['id', 'type', 'context', 'question', 'answer']
    with output_path.open('w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in standardized_data:
            writer.writerow(entry)
    print(f"Standardized data has been written to {output_file}")


def narrative_qa_normalizer():
    input_file = 'narrative_qa.csv'
    output_file = 'narrative_standardized.csv'

    input_path = CRUDE_DATA_FOLDER / input_file
    output_path = NORMALIZED_DATA_FOLDER / output_file

    standardized_data = []

    with input_path.open('r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            _id = row['document_id']
            question = row['question']
            answer1 = row['answer1']
            answer2 = row['answer2']
            combined_answers = f"{answer1} {answer2}"
            standardized_entry = {
                'id': _id,
                "type": row["set"],
                'context': f"{question} {combined_answers}",
                'question': question,
                'answer': {combined_answers}
            }
            standardized_data.append(standardized_entry)

    save_to_csv(standardized_data, output_file)


def qasper_normalizer():
    input_file_dev = 'qasper_dev.json'
    input_file_train = 'qasper_train.json'
    output_file = 'qasper_standardized.csv'

    input_path_dev = CRUDE_DATA_FOLDER / input_file_dev
    input_path_train = CRUDE_DATA_FOLDER / input_file_train
    output_path = NORMALIZED_DATA_FOLDER / output_file

    standardized_data = []

    def process_qasper_data(data):
        content = list(data.values())
        for document in content:
            for index, qa in enumerate(document['qas']):
                entry = {"question": "", "answer": "", "context": ""}
                question = qa.get('question', '')
                entry["question"] += question
                answer_data = qa.get('answers', [])
                if answer_data:
                    for answer_dict in answer_data:
                        context = " ".join(answer_dict["answer"]["evidence"])
                        answer_text = " ".join(answer_dict["answer"]["highlighted_evidence"])
                        entry["context"] += context
                        entry["answer"] += answer_text
                standardized_data.append(entry)

    with input_path_dev.open('r', encoding='utf-8') as file:
        data_dev = json.load(file)
        process_qasper_data(data_dev)

    with input_path_train.open('r', encoding='utf-8') as file:
        data_train = json.load(file)
        process_qasper_data(data_train)

    for idx, item in enumerate(standardized_data, start=1):
        item['id'] = idx

    save_to_csv(standardized_data, output_file)


def main():
    narrative_qa_normalizer()
    qasper_normalizer()


if __name__ == '__main__':
    main()
