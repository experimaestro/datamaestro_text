import os
from tqdm import tqdm
import gzip
from pathlib import Path


def auto_open(path: Path, mode: str):
    if path.suffix == ".gz":
        return gzip.open(path, mode)
    return path.open(mode)


class CountingWrapper:
    """Wrap a file object to count the actual compressed bytes read."""

    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.bytes_read = 0

    def read(self, size=-1):
        data = self.file_obj.read(size)
        self.bytes_read += len(data)
        return data

    def readline(self, size=-1):
        data = self.file_obj.readline(size)
        self.bytes_read += len(data)
        return data

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    def close(self):
        self.file_obj.close()

    def __getattr__(self, attr):
        return getattr(self.file_obj, attr)


class TQDMBytesReader:
    def __init__(self, file_obj, total_size, **tqdm_kwargs):
        self.file_obj = CountingWrapper(file_obj)
        self.tqdm = tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            **tqdm_kwargs,
        )

    def _update_progress(self):
        delta = self.file_obj.bytes_read - self.tqdm.n
        if delta > 0:
            self.tqdm.update(delta)

    def read(self, size=-1):
        data = self.file_obj.read(size)
        self._update_progress()
        return data

    def readline(self, size=-1):
        line = self.file_obj.readline(size)
        self._update_progress()
        return line

    def readlines(self, hint=-1):
        lines = self.file_obj.readlines(hint)
        self._update_progress()
        return lines

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    def close(self):
        self.tqdm.close()
        self.file_obj.close()

    def __getattr__(self, attr):
        # Delegate any other attribute to the underlying file object
        return getattr(self.file_obj, attr)


class TQDMFileReader:
    def __init__(self, filepath, mode="rt", file_opener=open, **tqdm_kwargs):
        self.filepath = filepath
        self.mode = mode
        self.file_opener = file_opener
        self.tqdm_kwargs = tqdm_kwargs

    def __enter__(self):
        self.file_obj = self.file_opener(self.filepath, self.mode)
        total_size = os.path.getsize(self.filepath)  # this is compressed size
        self.reader = TQDMBytesReader(
            self.file_obj, total_size=total_size, **self.tqdm_kwargs
        )
        return self.reader

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reader.close()
