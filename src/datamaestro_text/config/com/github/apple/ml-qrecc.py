# See documentation on https://datamaestro.readthedocs.io

import re
import json
from pathlib import Path
from datamaestro.definitions import Dataset, datatasks, datatags, dataset
from datamaestro.data.ml import Supervised
from datamaestro.download import reference
from datamaestro.download.archive import ZipDownloader
from datamaestro.download.wayback import wayback_documents
from datamaestro.utils import HashCheck
from datamaestro_text.data.conversation.qrecc import QReCCDataset
from datamaestro_text.datasets.irds.data import (
    LZ4JSONLDocumentStore,
    SimpleJsonDocument,
)
from datamaestro_text.datasets.irds.helpers import lz4docstore_builder


@datatags("conversation", "context", "query")
@datatasks("query rewriting")
@dataset(
    url="https://github.com/apple/ml-qrecc",
    doi="https://doi.org/10.48550/arXiv.2010.04898",
    id="",
)
class Main(Dataset):
    """Open-Domain Question Answering Goes Conversational via Question Rewriting

    We introduce QReCC (Question Rewriting in Conversational Context), an
    end-to-end open-domain question answering dataset comprising of 14K
    conversations with 81K question-answer pairs. The goal of this dataset is to
    provide a challenging benchmark for end-to-end conversational question
    answering that includes the individual subtasks of question rewriting,
    passage retrieval and reading comprehension
    """

    DATA = ZipDownloader(
        "data",
        "https://github.com/apple/ml-qrecc/raw/main/dataset/qrecc_data.zip",
        checker=HashCheck("f88fcc7ef3678cd6312080389c8abd67"),
    )

    def config(self) -> Supervised:
        return Supervised.C(
            train=QReCCDataset.C(path=self.DATA.path / "qrecc_train.json"),
            test=QReCCDataset.C(path=self.DATA.path / "qrecc_test.json"),
        )


@dataset(
    url="https://github.com/apple/ml-qrecc",
    doi="https://doi.org/10.48550/arXiv.2010.04898",
)
class Content(Dataset):
    """QReCC mentionned URLs content"""

    MAIN = reference(reference=Main)

    WAYBACK_DOCS = wayback_documents(
        "20191127",
        lambda: Content._urls(Content.MAIN.prepare()),
        name="wayback.jsonl",
    )

    STORE = lz4docstore_builder(
        "store",
        lambda: Content._documents(Content.WAYBACK_DOCS.path),
        SimpleJsonDocument,
        "id",
    )

    def config(self) -> LZ4JSONLDocumentStore:
        return LZ4JSONLDocumentStore.C(jsonl_path=self.STORE.path)

    @staticmethod
    def _documents(path: Path):
        """Iterates over documents from wayback"""
        with path.open("rt") as fp:
            for line in fp:
                yield SimpleJsonDocument(**json.loads(line))

    @staticmethod
    def _urls(supervised: Supervised[QReCCDataset, None, QReCCDataset]):
        urls = set()
        for ds in [supervised.train, supervised.test]:
            for entry in ds.entries():
                if entry.answer_url:
                    url = re.sub("#.*$", "", entry.answer_url)
                    urls.add(url)
        return urls
