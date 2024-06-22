import csv
from project_utils.unused_imports_generator._dependency_handler import (get_virtual_environment_current_packages,
                                                                        get_package_dependencies)
from project_utils.unused_imports_generator._project_files import get_all_import_statements
from project_utils.unused_imports_generator._unused_imports import get_unused_imports, organize_unused_imports_by_layers


def remove_subtree_dependencies(package_to_remove, package_dependencies):
    """Recursively find all dependencies of a package to remove."""
    packages_to_remove = set()
    packages_to_scan = [package_to_remove]
    while packages_to_scan:
        current_package = packages_to_scan.pop()
        packages_to_remove.add(current_package)
        for package, dependencies in package_dependencies.items():
            if package in packages_to_remove:
                continue  # Skip if already scheduled for removal
            if current_package in dependencies:
                packages_to_scan.append(package)
                packages_to_remove.add(package)
    return packages_to_remove


def filter_packages(layered_packages, package_dependencies, packages_to_ignore):
    """Filter out packages to ignore and their subtrees from the data."""
    all_packages_to_remove = set()
    for package in packages_to_ignore:
        all_packages_to_remove.update(remove_subtree_dependencies(package, package_dependencies))

    # Filter layered_packages
    filtered_layered_packages = {}
    for layer, packages in layered_packages.items():
        filtered_packages = [package for package in packages if package not in all_packages_to_remove]
        if filtered_packages:
            filtered_layered_packages[layer] = filtered_packages

    # Filter package_dependencies
    filtered_package_dependencies = {package: dependencies for package, dependencies in package_dependencies.items()
                                     if package not in all_packages_to_remove}

    return filtered_layered_packages, filtered_package_dependencies


def export_results_to_csv(layered_packages, package_dependencies, packages_to_ignore,
                          file_path='packages_depth.csv'):
    layered_packages, package_dependencies = filter_packages(layered_packages, package_dependencies, packages_to_ignore)

    max_dependencies = max((len(deps) for deps in package_dependencies.values()), default=0)
    header = ['package_name', 'package_depth'] + [f'package_dependency_{i}' for i in range(1, max_dependencies + 1)]

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)

        for layer, packages in layered_packages.items():
            for package in packages:
                dependencies = list(package_dependencies.get(package, []))
                csv_writer.writerow([package, layer] + dependencies + [''] * (max_dependencies - len(dependencies)))

    print(f"Exported to {file_path}")


def main():
    installed_packages = get_virtual_environment_current_packages()
    dependencies = get_package_dependencies()
    all_imports = get_all_import_statements()
    unused_packages = get_unused_imports(installed_packages, all_imports, dependencies)
    layered_dict = organize_unused_imports_by_layers(unused_packages, dependencies)
    packages_to_ignore = ["flask_socketio", "alembic"]
    export_results_to_csv(layered_dict, dependencies, packages_to_ignore)
    print("Unused Packages:", unused_packages)


if __name__ == "__main__":
    main()
