# See documentation on https://datamaestro.readthedocs.io

from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.download.archive import zipdownloader
from datamaestro.utils import HashCheck

from datamaestro.data.ml import Supervised
from datamaestro_text.data.conversation.canard import CanardDataset


@datatags("conversation", "context", "query")
@datatasks("query rewriting")
@zipdownloader(
    "archive",
    "https://obj.umiacs.umd.edu/elgohary/CANARD_Release.zip",
    subpath="CANARD_Release",
    checker=HashCheck("c9bba7c6bb898f669383415b54fd6ffd"),
)
@dataset(Supervised, url="https://sites.google.com/view/qanta/projects/canard", id="")
def main(archive):
    """Question-in-context rewriting

    CANARD is a dataset for question-in-context rewriting that consists of
    questions each given in a dialog context together with a context-independent
    rewriting of the question. The context of each question is the dialog
    utterances that precede the question. CANARD can be used to evaluate
    question rewriting models that handle important linguistic phenomena such as
    co-reference and ellipsis resolution.

    Each dataset is an instance of :class:`datamaestro_text.data.conversation.CanardDataset`
    """
    return {
        "train": CanardDataset(path=archive / "train.json"),
        "validation": CanardDataset(path=archive / "dev.json"),
        "test": CanardDataset(path=archive / "test.json"),
    }
