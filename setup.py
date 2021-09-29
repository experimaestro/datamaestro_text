from pathlib import Path
from setuptools import setup
import os

basepath = Path(__file__).parent

version = None
if os.environ.get("NO_GIT", 0) == "1":
    version = "0.0.0-dev"

setup(
    install_requires=(basepath / "requirements.txt").read_text(),
    use_scm_version=version is None,
    version=version,
)
