import csv
import re

import yaml
import subprocess
from typing import List

from business_logic.utils.commit_utils import get_commit_table
from business_logic.utils.date_utils import convert_to_american_date


def get_authors_emails(since_date: str, until_date: str) -> List[str]:
    since = convert_to_american_date(since_date)
    until = convert_to_american_date(until_date)
    command = f'git log --since="{since}" --until="{until}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    lines = result.stdout.split('\n')
    pattern = r'Author:.*<(.*)>'
    emails = [re.search(pattern, item).group(1) for item in lines if re.search(pattern, item)]
    unique_emails = list(set(email for email in emails if email.strip()))
    return unique_emails


def get_commit_diff(commit_ids: List[str]):
    commit_data = {}
    for commit_id in commit_ids[1:]:
        print(f'Getting commit {commit_id}')
        command = f'git show {commit_id}'
        result = subprocess.run(command, shell=True, capture_output=True)
        diff = result.stdout.decode('utf-8')
        commit_data[commit_id] = {'diff': diff, 'size': len(diff)}
    return commit_data


def output_to_yaml(data, filename):
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1]['totalChanges']))
    with open(filename, 'w') as file:
        yaml.dump(sorted_data, file, sort_keys=False)


def analysis_pipeline():
    sprints = [{"sprint": 1, "since_date": "07/mar", "until_date": "26/mar"},
               {"sprint": 2, "since_date": "22/mar", "until_date": "10/apr"},
               {"sprint": 3, "since_date": "10/apr", "until_date": "25/apr"},
               {"sprint": 4, "since_date": "26/apr", "until_date": "11/may"}]
    author_pool = get_authors_emails(since_date="01/jan", until_date="01/dec")
    for sprint in sprints:
        for author in author_pool:
            data = get_commit_table(author_email=author, since_date=sprint["since_date"], until_date=sprint["until_date"])
            output_to_yaml(data, f'sprint_{sprint["sprint"]}_{author}.yaml')
    # data = get_commit_table(author_email="mateus_b09@hotmail.com", since_date="07/mar", until_date="26/mar")
    # output_to_yaml(data, 'sprint_1_mateus.yaml')
    return


def main():
    # res = get_authors_emails("26/apr", "11/may")
    # print(res)
    analysis_pipeline()


if __name__ == '__main__':
    main()
