from datamaestro.definitions import Dataset, datatasks, datatags, dataset
from datamaestro.download.single import FileDownloader
from datamaestro.utils import HashCheck

from datamaestro.data.ml import Supervised
from datamaestro_text.data.conversation.canard import CanardDataset


@datatags("conversation", "context", "query")
@datatasks("query rewriting")
@dataset(url="https://sites.google.com/view/qanta/projects/canard", id="")
class Main(Dataset):
    """Question-in-context rewriting

    CANARD is a dataset for question-in-context rewriting that consists of
    questions each given in a dialog context together with a context-independent
    rewriting of the question. The context of each question is the dialog
    utterances that precede the question. CANARD can be used to evaluate
    question rewriting models that handle important linguistic phenomena such as
    co-reference and ellipsis resolution.

    Each dataset is an instance of :class:`datamaestro_text.data.conversation.CanardDataset`
    """

    TRAIN = FileDownloader(
        "train.json",
        "https://raw.githubusercontent.com/aagohary/canard/refs/heads/master/data/release/train.json",
        checker=HashCheck("73624ac646fb81e09b0fd7f01370ada3"),
    )
    DEV = FileDownloader(
        "dev.json",
        "https://raw.githubusercontent.com/aagohary/canard/refs/heads/master/data/release/dev.json",
        checker=HashCheck("c84525631a83bc771c58ff31f4a9b601"),
    )
    TEST = FileDownloader(
        "test.json",
        "https://raw.githubusercontent.com/aagohary/canard/refs/heads/master/data/release/test.json",
        checker=HashCheck("3fc14d0078e7a5056f5da571728f024e"),
    )

    def config(self) -> Supervised:
        return Supervised.C(
            train=CanardDataset.C(path=self.TRAIN.path),
            validation=CanardDataset.C(path=self.DEV.path),
            test=CanardDataset.C(path=self.TEST.path),
        )
