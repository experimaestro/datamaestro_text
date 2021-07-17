import logging
from typing import List, Union

logging.basicConfig(level=logging.INFO)

import os
import random
from pathlib import Path
import tempfile
from threading import Thread
from experimaestro import Task, Param, Annotated, pathgenerator, Option
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


def getpathname(context, config):
    name = "triplets.lst"
    if config.data.path.name.endswith(".gz"):
        name = "triplets.lst.gz"

    return context.currentpath() / name


class ShuffledTrainingTripletsLines(Task):
    data: Param[ir.TrainingTripletsLines]
    path: Annotated[Path, pathgenerator(getpathname)]
    seed: Param[int]
    compressed: Option[bool] = True

    def config(self):
        data = self.data.copy()
        data.path = self.path
        return data

    def execute(self):
        # --- Shuffle using the shuf command with a seed
        r = RandomStream(self.seed)
        stdin = subprocess.DEVNULL

        command: List[Union[str, Path]] = ["shuf", f"--random-source={r.filepath}"]

        if not self.compressed:
            command.extend(["-o", self.path])

        compressed = self.data.path.name.endswith(".gz")
        if compressed:
            stdin = subprocess.Popen(
                ["gunzip", "-c", self.data.path], stdout=subprocess.PIPE
            ).stdout
            command.append("-")
        else:
            command.append(self.data.path)

        # Output can be a stream or nothing
        stdout = None
        if self.compressed:
            output = self.path.open("w+")
            stdout = subprocess.Popen(
                ["gzip", "-c"], stdin=subprocess.PIPE, stdout=output
            ).stdin

        # Run the command
        p = subprocess.Popen(command, stdin=stdin, stdout=stdout)
        if stdin != subprocess.DEVNULL:
            stdin.close()

        with r:
            p.wait()
            assert p.returncode == 0
