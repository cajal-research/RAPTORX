import os
from pathlib import Path
from typing import List

SOURCE_FOLDER = Path(__file__).parent.parent.parent / "source"


def get_current_project_files() -> List[str]:
    """List all .py files in the current project."""
    files = []
    for root, _, filenames in os.walk(SOURCE_FOLDER):
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(os.path.join(root, filename))
    return files


def get_imports_from_file(file_path: str) -> List[str]:
    """Extract import statements from a given file."""
    with open(file_path, "r") as file:
        lines = file.readlines()
    imports = [line.strip() for line in lines if line.startswith("import") or line.startswith("from")]
    return imports


def get_all_import_statements():
    files = get_current_project_files()
    all_imports = []
    for file in files:
        imports = get_imports_from_file(file)
        all_imports.extend(imports)
    return all_imports


def main():
    all_imports = get_all_import_statements()
    print(all_imports)
    return


if __name__ == "__main__":
    main()
