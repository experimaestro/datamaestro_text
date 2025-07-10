# See documentation on https://datamaestro.readthedocs.io

import bz2
from datamaestro.download import reference
from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro_text.data.conversation.base import ConversationUserTopics
from datamaestro_text.data.ir import Adhoc

from datamaestro.utils import HashCheck
from datamaestro.context import DatafolderPath
from datamaestro.download.single import filedownloader
from datamaestro_text.data.conversation.ikat import IkatDataset
from datamaestro.download.links import linkfolder

from datamaestro_text.data.ir.stores import IKatClueWeb22DocumentStore
from datamaestro_text.data.ir.trec import TrecAdhocAssessments
from datamaestro_text.datasets.irds.helpers import lz4docstore_builder


@dataset(as_prepare=True)
def clueweb22(dataset, options=None) -> IKatClueWeb22DocumentStore:
    # Number of documents in the dataset
    count = 116_838_987

    jsonl_folder = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.ikat.clueweb22", "jsonl")]
    ).setup(dataset, options)
    store_path = lz4docstore_builder(
        "store",
        IKatClueWeb22DocumentStore.generator(
            jsonl_folder,
            ".jsonl.bz2",
            opener=bz2.open,
            num_files=16,
            checker=HashCheck("70245f7ce292175c66f48eebb7b4a71d"),
        ),
        IKatClueWeb22DocumentStore.Document,
        "id",
        count_hint=count,
    ).setup(dataset, options)

    return IKatClueWeb22DocumentStore.C(path=store_path, count=count)


@datatags("conversation", "context", "query")
@datatasks("conversational search", "query rewriting")
@reference("documents", clueweb22)
@filedownloader(
    "topics.json",
    "https://raw.githubusercontent.com/irlabamsterdam/iKAT/refs/heads/main/2025/data/2025_test_topics.json",
    checker=HashCheck("684fa0197cdec8c3cfb6a2e586ab83f6"),
)
@dataset(
    id="2025",
    url="https://github.com/irlabamsterdam/iKAT/tree/main/2025",
)
def test_2025(topics, documents) -> Adhoc.C:
    """Question-in-context rewriting

    iKAT is a test dataset for question-in-context rewriting that consists of
    questions each given in a dialog context together with a context-independent
    rewriting of the question.
    """
    return Adhoc.C(
        topics=ConversationUserTopics.C(conversations=IkatDataset.C(path=topics)),
        # TODO: add when available
        assessments=TrecAdhocAssessments(path="/to/do"),
        documents=documents,
    )


@datatags("conversation", "context", "query")
@datatasks("conversational search", "query rewriting")
@reference("documents", clueweb22)
@filedownloader(
    "qrels",
    "https://trec.nist.gov/data/ikat/2023-qrels.all-turns.txt",
    checker=HashCheck("79dc121bab25b2245e52a53263e5ad1f"),
)
@filedownloader(
    "topics.json",
    "https://raw.githubusercontent.com/irlabamsterdam/iKAT/refs/heads/main/2023/data/2023_test_topics.json",
    checker=HashCheck("684fa0197cdec8c3cfb6a2e586ab83f6"),
)
@dataset(
    Adhoc,
    id="2023",
    url="https://github.com/irlabamsterdam/iKAT/tree/main/2023",
)
def test_2023(topics, qrels, documents) -> Adhoc.C:
    """iKAT 2023 dataset"""
    return Adhoc.C(
        topics=ConversationUserTopics.C(conversations=IkatDataset.C(path=topics)),
        assessments=TrecAdhocAssessments.C(path=qrels),
        documents=documents,
    )
