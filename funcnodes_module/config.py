import os

template_path = os.path.join(os.path.dirname(__file__), "template_folder")
files_to_overwrite = [
    os.path.join(".github", "workflows", "py_test.yml"),
    os.path.join(".github", "workflows", "version_publish_main.yml"),
    os.path.join(".github", "actions", "cache_py", "action.yml"),
    os.path.join(".github", "actions", "updates_version", "action.yml"),
    os.path.join(".github", "actions", "install_package", "action.yml"),
    os.path.join("tests", "all_nodes_test_base.py"),
]

files_to_copy_if_missing = [
    os.path.join("tests", "test_all_nodes.py"),
    os.path.join(".pre-commit-config.yaml"),
]


package_requirements = [
    "funcnodes@*",
]

dev_requirements = [
    "pre-commit@*",
    "pytest@*",
    "funcnodes-module@*",
]

gitpaths = [
    ".github",
    ".git",
]
