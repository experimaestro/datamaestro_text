# See documentation on https://datamaestro.readthedocs.io

from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.download.single import filedownloader
from datamaestro.utils import HashCheck


from datamaestro_text.data.conversation.orconvqa import OrConvQADataset
from datamaestro.data.ml import Supervised


@datatags("conversation", "context", "query")
@datatasks("query rewriting")
@filedownloader(
    "train.jsonl",
    "https://ciir.cs.umass.edu/downloads/ORConvQA/preprocessed/train.txt",
    checker=HashCheck("7513a9ef12d8b7a4471166dc4fef77b7"),
)
@filedownloader(
    "dev.jsonl",
    "https://ciir.cs.umass.edu/downloads/ORConvQA/preprocessed/dev.txt",
    checker=HashCheck("7765658995cc9ffd5eb39a400d814b20"),
)
@filedownloader(
    "test.jsonl",
    "https://ciir.cs.umass.edu/downloads/ORConvQA/preprocessed/test.txt",
    checker=HashCheck("0cf3a755f06297b9c02e7db45f8dc8be"),
)
@dataset(
    Supervised,
    url="https://github.com/prdwb/orconvqa-release",
)
def preprocessed(train, dev, test):
    """Question-in-context rewriting

    CANARD is a dataset for question-in-context rewriting that consists of
    questions each given in a dialog context together with a context-independent
    rewriting of the question. The context of each question is the dialog
    utterances that precede the question. CANARD can be used to evaluate
    question rewriting models that handle important linguistic phenomena such as
    co-reference and ellipsis resolution.

    Each dataset is an instance of :class:`datamaestro_text.data.conversation.OrConvQADataset`
    """
    return {
        "train": OrConvQADataset(path=train),
        "validation": OrConvQADataset(path=dev),
        "test": OrConvQADataset(path=test),
    }
