import os
import json
from pathlib import Path

CURRENT_FOLDER = "source/models"


def build_directory_structure(root_directory):
    IGNORED_FOLDERS = [".pytest_cache", "versions", "__pycache__"]
    structure = []
    for item in sorted(os.listdir(root_directory)):
        if item in IGNORED_FOLDERS or item.startswith('.'):
            continue
        item_path = os.path.join(root_directory, item)
        if os.path.isdir(item_path):
            # Recursively build structure for directories
            structure.append({item: build_directory_structure(item_path)})
        else:
            # Add files directly into the structure list
            structure.append(item)
    return structure


def main():
    root_folder_dir = Path(__file__).parent.parent.parent
    source_dir = root_folder_dir / CURRENT_FOLDER
    directory_structure = build_directory_structure(source_dir)
    with open('directory_structure.json', 'w') as f:
        json.dump(directory_structure, f, indent=4)
    print("Directory structure has been output to directory_structure.json")


if __name__ == "__main__":
    main()
