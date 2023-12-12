# See documentation on https://datamaestro.readthedocs.io

from collections import namedtuple
import gzip
import json
from pathlib import Path
from typing import Iterator, NamedTuple
import attrs
from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.download.single import filedownloader
from datamaestro.utils import HashCheck


from datamaestro_text.data.conversation.orconvqa import OrConvQADataset
from datamaestro.data.ml import Supervised

from datamaestro_text.data.ir import DocumentStore
from datamaestro_text.data.ir.formats import OrConvQADocument
from datamaestro_text.data.ir.stores import OrConvQADocumentStore
from datamaestro_text.datasets.irds.data import LZ4DocumentStore
from datamaestro_text.datasets.irds.helpers import lz4docstore_downloader


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
    """Open-Retrieval Conversational Question Answering datasets

    OrConvQA is an aggregation of three existing datasets:

    1. the QuAC dataset that offers information-seeking conversations,
    1. the CANARD dataset that consists of context-independent rewrites of QuAC questions, and
    3. the Wikipedia corpus that serves as the knowledge source of answering questions.

    Each dataset is an instance of :class:`datamaestro_text.data.conversation.OrConvQADataset`
    """
    return {
        "train": OrConvQADataset(path=train),
        "validation": OrConvQADataset(path=dev),
        "test": OrConvQADataset(path=test),
    }


def orConvQADocumentReader(source: Path) -> Iterator[OrConvQADocumentStore.NAMED_TUPLE]:
    with gzip.open(source, "rt") as fp:
        for line in fp:
            yield OrConvQADocumentStore.NAMED_TUPLE(**json.loads(line))


@lz4docstore_downloader(
    "all_blocks",
    "https://ciir.cs.umass.edu/downloads/ORConvQA/all_blocks.txt.gz",
    orConvQADocumentReader,
    OrConvQADocumentStore.NAMED_TUPLE,
    "id",
    checker=HashCheck("1095a3408690e7bbe4d8a87a2bae6356"),
    size=5_086_902_800,
    count_hint=11_377_951,
)
@dataset(
    OrConvQADocumentStore,
    url="https://github.com/prdwb/orconvqa-release",
)
def passages(all_blocks):
    """orConvQA wikipedia files

    OrConvQA is an aggregation of three existing datasets:

    1. the QuAC dataset that offers information-seeking conversations,
    1. the CANARD dataset that consists of context-independent rewrites of QuAC questions, and
    3. the Wikipedia corpus that serves as the knowledge source of answering questions.
    """
    return {"path": all_blocks, "count": 11_377_951}
