import logging

logging.basicConfig(level=logging.INFO)

import os
import random
from pathlib import Path
import tempfile
from threading import Thread
from experimaestro import Task, Param, Annotated, pathgenerator
import datamaestro_text.data.ir as ir
import subprocess


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


class ShuffledTrainingTripletsLines(Task):
    data: Param[ir.TrainingTripletsLines]
    path: Annotated[Path, pathgenerator("triplets.lst")]
    seed: Param[int]

    def config(self):
        data = self.data.copy()
        data.path = self.path
        return data

    def execute(self):
        # --- Shuffle using the shuf command with a seed
        r = RandomStream(self.seed)
        command = [
            "shuf",
            f"--random-source={r.filepath}",
            "-o",
            self.path,
            self.data.path,
        ]
        p = subprocess.Popen(command)
        with r:
            p.wait()
            assert p.returncode == 0
