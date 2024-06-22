from typing import List, Set

from project_utils.unused_imports_generator._dependency_handler import normalize_package_name, \
    get_virtual_environment_current_packages, get_package_dependencies
from project_utils.unused_imports_generator._project_files import get_all_import_statements


def get_unused_imports(venv_packages: dict[str, str], imports: List[str],
                       dependencies: dict[str, Set[str]]) -> List[str]:
    """
    Identify unused packages, considering package dependencies.
    """
    imported_packages = set()
    installed_packages = set(venv_packages.keys())
    used_packages = set()

    # Normalize and gather all import names for comparison
    for line in imports:
        current_package = ""
        if line.startswith("import "):
            current_package = line.split("import ")[1].split(".")[0].split(" as ")[0]
        elif line.startswith("from "):
            current_package = line.split("from ")[1].split(" import")[0].split(".")[0]
        if current_package:
            normalized_package = normalize_package_name(current_package)
            imported_packages.add(normalized_package)
            used_packages.add(normalized_package)

    # Determine unused packages
    unused_packages = installed_packages - used_packages

    return sorted(list(unused_packages))


def organize_unused_imports_by_layers(unused_imports: List[str], package_dependencies: dict[str, Set[str]]) -> dict[
    int, List[str]]:
    """
    Organize unused imports by dependency layers.

    :param unused_imports: A list of unused package names.
    :param package_dependencies: A dictionary where keys are package names and values are sets of packages they depend on.
    :return: A dictionary where keys are dependency layers (0, 1, ...) and values are lists of packages at those layers.
    """
    # Reverse the dependency mapping for easier processing
    reverse_dependencies = {}
    for package, dependencies in package_dependencies.items():
        for dep in dependencies:
            reverse_dependencies.setdefault(dep, set()).add(package)

    # Initialize the layering process
    layers = {}
    processed = set()

    def assign_layer(_package, layer):
        """Recursively assign packages to layers based on their dependency level."""
        if _package in processed:
            return
        processed.add(_package)
        layers.setdefault(layer, []).append(_package)
        for dependent in reverse_dependencies.get(_package, []):
            assign_layer(dependent, layer + 1)

    # Assign each unused import to a layer
    for package in unused_imports:
        if package not in processed:
            assign_layer(package, 0)

    # Ensure that only unused imports are included in the final layering
    final_layers = {layer: [pkg for pkg in pkgs if pkg in unused_imports] for layer, pkgs in layers.items()}

    max_layer = max(layers.keys(), default=0)
    inverted_layers = {}
    for layer, pkgs in final_layers.items():
        inverted_layers[max_layer - layer] = pkgs

    return inverted_layers


def main():
    installed_packages = get_virtual_environment_current_packages()
    all_imports = get_all_import_statements()
    dependencies = get_package_dependencies()
    unused_packages = get_unused_imports(installed_packages, all_imports, dependencies)
    return


if __name__ == "__main__":
    main()
