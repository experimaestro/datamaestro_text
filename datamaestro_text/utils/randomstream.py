import tempfile
import os
import random
import logging
from pathlib import Path
from threading import Thread


class RandomStream(Thread):
    """Generate a FIFO file with random bytes"""

    def __init__(self, seed: int):
        super().__init__()
        tmpdir = tempfile.mkdtemp()
        self.filepath = Path(tmpdir) / "random"
        os.mkfifo(self.filepath)
        self.random = random.Random(seed)
        self.thread = None

    def run(self):
        logging.info("Starting to write random bytes %s", self.filepath)
        try:
            with self.filepath.open("wb") as out:
                while True:
                    data = bytearray(random.getrandbits(8) for _ in range(256))
                    out.write(data)
        except BrokenPipeError:
            pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.join()
        self.filepath.unlink()
        self.filepath.parent.rmdir()
