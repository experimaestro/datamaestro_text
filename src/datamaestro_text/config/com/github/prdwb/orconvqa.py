# See documentation on https://datamaestro.readthedocs.io

import gzip
import json
from pathlib import Path
from typing import Iterator
from datamaestro.definitions import Dataset, datatasks, datatags, dataset
from datamaestro.download.single import FileDownloader
from datamaestro.utils import HashCheck


from datamaestro_text.data.conversation.orconvqa import OrConvQADataset
from datamaestro.data.ml import Supervised

from datamaestro_text.data.ir.stores import OrConvQADocumentStore
from datamaestro_text.datasets.irds.helpers import lz4docstore_downloader


@datatags("conversation", "context", "query")
@datatasks("query rewriting")
@dataset(
    url="https://github.com/prdwb/orconvqa-release",
)
class Preprocessed(Dataset):
    """Open-Retrieval Conversational Question Answering datasets

    OrConvQA is an aggregation of three existing datasets:

    1. the QuAC dataset that offers information-seeking conversations,
    1. the CANARD dataset that consists of context-independent rewrites of QuAC questions, and
    3. the Wikipedia corpus that serves as the knowledge source of answering questions.

    Each dataset is an instance of :class:`datamaestro_text.data.conversation.OrConvQADataset`
    """

    TRAIN = FileDownloader(
        "train.jsonl",
        "https://ciir.cs.umass.edu/downloads/ORConvQA/preprocessed/train.txt",
        checker=HashCheck("7513a9ef12d8b7a4471166dc4fef77b7"),
    )
    DEV = FileDownloader(
        "dev.jsonl",
        "https://ciir.cs.umass.edu/downloads/ORConvQA/preprocessed/dev.txt",
        checker=HashCheck("7765658995cc9ffd5eb39a400d814b20"),
    )
    TEST = FileDownloader(
        "test.jsonl",
        "https://ciir.cs.umass.edu/downloads/ORConvQA/preprocessed/test.txt",
        checker=HashCheck("0cf3a755f06297b9c02e7db45f8dc8be"),
    )

    def config(self) -> Supervised:
        return Supervised.C(
            train=OrConvQADataset.C(path=self.TRAIN.path),
            validation=OrConvQADataset.C(path=self.DEV.path),
            test=OrConvQADataset.C(path=self.TEST.path),
        )


def orConvQADocumentReader(source: Path) -> Iterator[OrConvQADocumentStore.NAMED_TUPLE]:
    with gzip.open(source, "rt") as fp:
        for line in fp:
            data = json.loads(line)
            data["body"] = data.pop("text")
            yield OrConvQADocumentStore.NAMED_TUPLE(**data)


@dataset(
    url="https://github.com/prdwb/orconvqa-release",
)
class Passages(Dataset):
    """orConvQA wikipedia files

    OrConvQA is an aggregation of three existing datasets:

    1. the QuAC dataset that offers information-seeking conversations,
    1. the CANARD dataset that consists of context-independent rewrites of QuAC questions, and
    3. the Wikipedia corpus that serves as the knowledge source of answering questions.
    """

    ALL_BLOCKS = lz4docstore_downloader(
        "all_blocks",
        "https://ciir.cs.umass.edu/downloads/ORConvQA/all_blocks.txt.gz",
        orConvQADocumentReader,
        OrConvQADocumentStore.NAMED_TUPLE,
        "id",
        checker=HashCheck("1095a3408690e7bbe4d8a87a2bae6356"),
        size=5_086_902_800,
        count_hint=11_377_951,
    )

    def config(self) -> OrConvQADocumentStore:
        return OrConvQADocumentStore.C(path=self.ALL_BLOCKS.path, count=11_377_951)
