import gzip
from pathlib import Path


def auto_open(path: Path, mode: str):
    if path.suffix == ".gz":
        return gzip.open(path, mode)
    return path.open(mode)
