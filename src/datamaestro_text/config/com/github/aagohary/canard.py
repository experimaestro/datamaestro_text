from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.download.single import filedownloader
from datamaestro.utils import HashCheck

from datamaestro.data.ml import Supervised
from datamaestro_text.data.conversation.canard import CanardDataset


@datatags("conversation", "context", "query")
@datatasks("query rewriting")
@filedownloader(
    "train.json",
    "https://raw.githubusercontent.com/aagohary/canard/refs/heads/master/data/release/train.json",
    checker=HashCheck("73624ac646fb81e09b0fd7f01370ada3"),
)
@filedownloader(
    "dev.json",
    "https://raw.githubusercontent.com/aagohary/canard/refs/heads/master/data/release/dev.json",
    checker=HashCheck("c84525631a83bc771c58ff31f4a9b601"),
)
@filedownloader(
    "test.json",
    "https://raw.githubusercontent.com/aagohary/canard/refs/heads/master/data/release/test.json",
    checker=HashCheck("3fc14d0078e7a5056f5da571728f024e"),
)
@dataset(Supervised, url="https://sites.google.com/view/qanta/projects/canard", id="")
def main(train, dev, test):
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
        "train": CanardDataset(path=train),
        "validation": CanardDataset(path=dev),
        "test": CanardDataset(path=test),
    }
