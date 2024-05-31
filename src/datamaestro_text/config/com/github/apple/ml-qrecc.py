# See documentation on https://datamaestro.readthedocs.io

from pathlib import Path
from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.data.ml import Supervised
from datamaestro.download.archive import zipdownloader
from datamaestro.utils import HashCheck
from datamaestro_text.data.conversation.qrecc import QReCCDataset


@datatags("conversation", "context", "query")
@datatasks("query rewriting")
@zipdownloader(
    "data",
    "https://github.com/apple/ml-qrecc/raw/main/dataset/qrecc_data.zip",
    checker=HashCheck("f88fcc7ef3678cd6312080389c8abd67"),
)
@dataset(
    Supervised[QReCCDataset, None, QReCCDataset],
    url="https://github.com/apple/ml-qrecc",
    doi="https://doi.org/10.48550/arXiv.2010.04898",
    id="",
)
def main(data: Path):
    """Open-Domain Question Answering Goes Conversational via Question Rewriting

    We introduce QReCC (Question Rewriting in Conversational Context), an
    end-to-end open-domain question answering dataset comprising of 14K
    conversations with 81K question-answer pairs. The goal of this dataset is to
    provide a challenging benchmark for end-to-end conversational question
    answering that includes the individual subtasks of question rewriting,
    passage retrieval and reading comprehension
    """
    return {
        "train": QReCCDataset(path=data / "qrecc_train.json"),
        "test": QReCCDataset(path=data / "qrecc_test.json"),
    }
