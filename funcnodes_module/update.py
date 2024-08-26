import os
import shutil
from .utils import create_names, replace_names, read_file_content, write_file_content
from .config import (
    template_path,
    files_to_overwrite,
    files_to_copy_if_missing,
    dev_requirements,
    package_requirements,
)
from ._git import _init_git


def update_project(path, nogit=False):
    # check if path is a project
    path = os.path.abspath(path)

    if not os.path.exists(path):
        raise RuntimeError(f"Path {path} does not exist")

    if not os.path.isdir(path):
        raise RuntimeError(f"Path {path} is not a directory")

    if not os.path.exists(os.path.join(path, "pyproject.toml")):
        raise RuntimeError(f"Path {path} is not a project")

    name = os.path.basename(path)
    project_name, module_name, package_name = create_names(name)

    if not os.path.exists(os.path.join(path, module_name)):
        print(f"Cant find module {module_name} in project {name}")
        return
    # check if funcnodes is in the project

    content, _ = read_file_content(os.path.join(path, "pyproject.toml"))
    if "funcnodes" not in content:
        print(f"Project at {path} does not seem to be a funcnodes project")
        return

    for file in files_to_overwrite:
        filepath = os.path.join(path, file)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        shutil.copy2(os.path.join(template_path, file), filepath)
        content, enc = read_file_content(filepath)

        content = replace_names(
            content,
            project_name=project_name,
            module_name=module_name,
            package_name=package_name,
        )
        write_file_content(filepath, content, enc)

    for file in files_to_copy_if_missing:
        if not os.path.exists(os.path.join(path, file)):
            filepath = os.path.join(path, file)
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
            shutil.copy2(os.path.join(template_path, file), filepath)
            content, enc = read_file_content(filepath)
            content = replace_names(
                content,
                project_name=project_name,
                module_name=module_name,
                package_name=package_name,
            )
            write_file_content(filepath, content, enc)

    # update requirements
    os.system(f"poetry add {' '.join(dev_requirements)} --group=dev")
    os.system(f"poetry add {' '.join(package_requirements)}")

    # update plugins in toml
    content, enc = read_file_content(os.path.join(path, "pyproject.toml"))
    if '[tool.poetry.plugins."funcnodes.module"]' not in content:
        content += (
            '\n[tool.poetry.plugins."funcnodes.module"]\n'
            f'module = "{name}"\n'
            f'shelf = "{name}:NODE_SHELF"\n'
        )
        write_file_content(os.path.join(path, "pyproject.toml"), content, enc)

        # remove the .git and .gitignore
    # check if the project is already in git
    if not os.path.exists(os.path.join(path, ".git")) and not nogit:
        _init_git(path)
    else:
        os.system("poetry update")
        os.system("poetry run pre-commit install")
        os.system("poetry run pre-commit autoupdate")

    # check if the git branch dev and test exist
    current_dir = os.getcwd()
    os.chdir(path)
    branches = [
        s.strip().strip("*").strip()
        for s in os.popen("git branch").read().strip().split("\n")
    ]
    if "dev" not in branches:
        os.system("git reset")
        os.system("git checkout -b dev")
        os.system('git commit --allow-empty -m "initial commit"')

    if "test" not in branches:
        os.system("git reset")
        os.system("git checkout -b test")
        os.system('git commit --allow-empty -m "initial commit"')

    os.chdir(current_dir)
