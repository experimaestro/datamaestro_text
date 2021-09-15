import logging
from typing import BinaryIO, List, Union

from xpmir.utils import StreamGenerator

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
    if config.compressed:
        name = "triplets.lst.gz"

    return context.currentpath() / name


class ShuffledTrainingTripletsLines(Task):
    data: Param[ir.TrainingTriplets]
    path: Annotated[Path, pathgenerator(getpathname)]
    seed: Param[int]
    compressed: Option[bool] = True

    def config(self):
        return ir.TrainingTripletsLines(
            id="", path=self.path, ids=self.data.ids, sep="\t"
        )

    def execute(self):
        # --- Shuffle using the shuf command with a seed
        r = RandomStream(self.seed)
        stdin = subprocess.DEVNULL

        command: List[Union[str, Path]] = ["shuf", f"--random-source={r.filepath}"]

        if not self.compressed:
            command.extend(["-o", self.path])
        command.append("-")

        def triplegenerator(out: BinaryIO):
            logging.info("Starting to output triples")
            count = 0

            for qid, doca, docb in self.data.iter():
                out.write(f"{qid}\t{doca}\t{docb}\n".encode("utf-8"))
                count += 1

            logging.info("Triples output ended (%d triples)", count)

        logging.info("Creating generator")
        generator = StreamGenerator(triplegenerator, mode="wb")

        # Output can be a stream or nothing
        stdout = None
        if self.compressed:
            output = self.path.open("w+")
            stdout = subprocess.Popen(
                ["gzip", "-c"], stdin=subprocess.PIPE, stdout=output
            ).stdin

        # Run the command
        with generator as _:
            logging.info("Starting to shuffle")
            with generator.filepath.open("rb") as stdin:
                p = subprocess.Popen(command, stdin=stdin, stdout=stdout)

            with r:
                p.wait()
                assert p.returncode == 0
