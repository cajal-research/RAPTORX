from typing import List


def flatten_and_concat_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_and_concat_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if all(isinstance(i, dict) for i in v):
                for i, item in enumerate(v):
                    items.extend(flatten_and_concat_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
            elif all(isinstance(i, str) for i in v):
                concatenated_str = ' '.join(v)
                items.append((new_key, concatenated_str))
            else:
                items.append((new_key, v))
        else:
            items.append((new_key, v))
    return dict(items)