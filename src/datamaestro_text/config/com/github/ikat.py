# See documentation on https://datamaestro.readthedocs.io

from datamaestro.download import reference
from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro_text.data.conversation.base import ConversationUserTopics
from datamaestro_text.data.ir import Adhoc

from datamaestro.utils import HashCheck
from datamaestro.context import DatafolderPath
from datamaestro.download.single import FileDownloader
from datamaestro_text.data.conversation.ikat import IkatConversations
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
            jsonl_folder / "ikat_2023_passages_jsonl.sha256sums",
            jsonl_folder / "ikat_2023_passages_hashes.tsv.bz2",
        ),
        IKatClueWeb22DocumentStore.Document,
        "id",
        count_hint=count,
    ).setup(dataset, options)

    return IKatClueWeb22DocumentStore.C(path=store_path, count=count)


@datatags("conversation", "context", "query")
@datatasks("conversational search", "query rewriting")
@dataset(
    id="2025",
    url="https://github.com/irlabamsterdam/iKAT/tree/main/2025",
)
class Test2025(Adhoc):
    """Question-in-context rewriting

    iKAT is a test dataset for question-in-context rewriting that consists of
    questions each given in a dialog context together with a context-independent
    rewriting of the question.
    """

    DOCUMENTS = reference(varname="documents", reference=clueweb22)
    TOPICS = FileDownloader(
        "topics.json",
        "https://raw.githubusercontent.com/irlabamsterdam/iKAT/refs/heads/main/2025/data/2025_test_topics.json",
        checker=HashCheck("16f8444a8d0a8dfe0090f478f185a63c"),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return Adhoc.C(
            topics=ConversationUserTopics.C(
                conversations=IkatConversations.C(path=cls.TOPICS.path)
            ),
            # TODO: add when available
            assessments=TrecAdhocAssessments.C(path="/to/do"),
            documents=cls.DOCUMENTS.prepare(),
        )


@datatags("conversation", "context", "query")
@datatasks("conversational search", "query rewriting")
@dataset(
    id="2024",
    url="https://github.com/irlabamsterdam/iKAT/tree/main/2024",
)
class Test2024(Adhoc):
    """iKAT 2024 dataset"""

    DOCUMENTS = reference(varname="documents", reference=clueweb22)
    QRELS = FileDownloader(
        "qrels",
        "https://trec.nist.gov/data/ikat/2024-qrels.txt",
        checker=HashCheck("57f958903ed1c12bbac207f62800814f"),
    )
    TOPICS = FileDownloader(
        "topics.json",
        "https://raw.githubusercontent.com/irlabamsterdam/iKAT/refs/heads/main/2024/data/2024_test_topics.json",
        checker=HashCheck("ad45bc6e7add2081d69ea60a0a4d1203"),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return Adhoc.C(
            topics=ConversationUserTopics.C(
                conversations=IkatConversations.C(path=cls.TOPICS.path)
            ),
            assessments=TrecAdhocAssessments.C(path=cls.QRELS.path),
            documents=cls.DOCUMENTS.prepare(),
        )


@datatags("conversation", "context", "query")
@datatasks("conversational search", "query rewriting")
@dataset(
    id="2023",
    url="https://github.com/irlabamsterdam/iKAT/tree/main/2023",
)
class Test2023(Adhoc):
    """iKAT 2023 dataset"""

    DOCUMENTS = reference(varname="documents", reference=clueweb22)
    QRELS = FileDownloader(
        "qrels",
        "https://trec.nist.gov/data/ikat/2023-qrels.all-turns.txt",
        checker=HashCheck("79dc121bab25b2245e52a53263e5ad1f"),
    )
    TOPICS = FileDownloader(
        "topics.json",
        "https://raw.githubusercontent.com/irlabamsterdam/iKAT/refs/heads/main/2023/data/2023_test_topics.json",
        checker=HashCheck("684fa0197cdec8c3cfb6a2e586ab83f6"),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return Adhoc.C(
            topics=ConversationUserTopics.C(
                conversations=IkatConversations.C(path=cls.TOPICS.path)
            ),
            assessments=TrecAdhocAssessments.C(path=cls.QRELS.path),
            documents=cls.DOCUMENTS.prepare(),
        )
