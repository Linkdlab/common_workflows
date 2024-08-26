import os
import tempfile
from .utils import read, replace_names, read_file_content, write_file_content


def check_funcnodes_module():
    # check that [tool.poetry.plugins."funcnodes.module"] exists in pyproject.toml
    content, _ = read_file_content("pyproject.toml")
    if '[tool.poetry.plugins."funcnodes.module"]' not in content:
        raise ValueError("funcnodes.module missing pyproject.toml")


def funcnodes_module_name():
    content, _ = read_file_content("pyproject.toml")
    correct_block = False
    for line in content.split("\n"):
        if line.startswith("["):
            correct_block = False
            if line == "[tool.poetry]":
                correct_block = True

        if line.startswith("name=") or line.startswith("name ="):
            if correct_block:
                return line.split("=")[1].strip().strip('"').replace("_", "-")
    raise ValueError("Could not find name in pyproject.toml")


def check_for_register(path):
    opath = os.getcwd()
    os.chdir(path)

    check_funcnodes_module()

    module_name = funcnodes_module_name()

    os.chdir(opath)
