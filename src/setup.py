from pathlib import Path
from setuptools import setup, find_packages

from .dependencies import load_dependencies_from_pipfile

pipfile_path = Path(__file__).parent.parent / "Pipfile"
ignore = {"jupyter", "matplotlib", "numpy", "pandas", "toml"}

setup(
    name='cluster_analysis',
    version='0.1',
    packages=find_packages(),
    install_requires=load_dependencies_from_pipfile(pipfile_path, ignore)
)
