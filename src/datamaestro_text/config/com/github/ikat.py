# See documentation on https://datamaestro.readthedocs.io

from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.data.ml import Supervised
from datamaestro.data import Base

from datamaestro.utils import HashCheck
from datamaestro.download.single import filedownloader
from datamaestro_text.data.conversation.ikat import IkatDatasetEntry, IkatDataset
from datamaestro_text.datasets.irds.data import (
    SimpleJsonDocument,
    LZ4JSONLDocumentStore,
)
import logging

@datatags("conversation", "context", "query")
@datatasks("query rewriting")
@filedownloader(
    "test.json",
    "https://raw.githubusercontent.com/irlabamsterdam/iKAT/refs/heads/main/2025/data/2025_test_topics.json",
    checker=HashCheck("16f8444a8d0a8dfe0090f478f185a63c"),
)

@dataset(
    Base,
    url="https://github.com/irlabamsterdam/iKAT/tree/main/2025",
)

def main(test) -> Supervised[IkatDataset, None, IkatDataset]:
    """Question-in-context rewriting

    iKAT is a test dataset for question-in-context rewriting that consists of 
    questions each given in a dialog context together with a context-independent
    rewriting of the question. 
    One of the special features of iKAT is that it includes a Personal PKTB', 
    """
    logging.info("Creating iKAT dataset from %s", test)
    return IkatDataset.C(path=test)