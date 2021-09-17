import logging
import gzip
from pathlib import Path
from experimaestro import Task, Param, Annotated, pathgenerator, Option
import datamaestro_text.data.ir as ir
from datamaestro_text.utils.shuffle import shuffle


def getpathname(context, config):
    name = "triplets.lst"
    if config.compressed:
        name = "triplets.lst.gz"

    return context.currentpath() / name


class ShuffledTrainingTripletsLines(Task):
    """Shuffle a set of training triplets"""

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

        def triplegenerator():
            logging.info("Starting to output triples")
            count = 0

            for qid, doca, docb in self.data.iter():
                yield f"{qid}\t{doca}\t{docb}\n"
                count += 1

            logging.info("Triples output ended (%d triples)", count)

        logging.info("Creating generator")

        # Output can be a stream or nothing
        if self.compressed:
            output = gzip.open(self.path, "wt")
        else:
            output = self.path.open("wt")

        with output:
            shuffle(triplegenerator(), output)
