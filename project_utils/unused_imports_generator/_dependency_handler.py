import json
import subprocess
from pathlib import Path


def normalize_package_name(name: str) -> str:
    """Normalize package names for comparison."""
    return name.lower().replace('-', '_')


def get_virtual_environment_current_packages() -> dict[str, str]:
    """Get current packages in the virtual environment."""
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    packages = result.stdout.splitlines()
    package_dict = {}
    for package in packages:
        package_name, package_version = package.split("==")
        package_dict[normalize_package_name(package_name)] = package_version
    return package_dict


def get_package_dependencies() -> dict[str, set]:
    """Get a mapping of dependencies to sets of packages that require them, with caching."""
    dependencies_file = Path("dependencies.json")

    if dependencies_file.exists():
        with open(dependencies_file, "r", encoding="utf-8") as file:
            dependencies = {dep: set(packages) for dep, packages in json.load(file).items()}
            return dependencies

    packages = get_virtual_environment_current_packages()
    dependencies = {}

    for package in packages.keys():
        try:
            print(f"Getting dependencies for: {package}")
            result = subprocess.run(["pip", "show", package], capture_output=True, text=True, encoding='utf-8',
                                    errors='ignore')

            for line in result.stdout.splitlines():
                if line.startswith("Requires:"):
                    deps = line.replace("Requires:", "").strip().split(", ")
                    for dep in deps:
                        normalized_dep = normalize_package_name(dep)
                        if normalized_dep:
                            if normalized_dep in dependencies:
                                dependencies[normalized_dep].add(package)
                            else:
                                dependencies[normalized_dep] = {package}
        except subprocess.CalledProcessError:
            print(f"Failed to get dependencies for package: {package}")
            continue
        except AttributeError:
            print(f"Failed to get dependencies for package: {package}")
            continue

    with open(dependencies_file, "w", encoding="utf-8") as file:
        json.dump({dep: list(packages) for dep, packages in dependencies.items()}, file)

    return dependencies
