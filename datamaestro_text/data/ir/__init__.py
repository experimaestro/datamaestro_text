"""Generic data types for information retrieval"""

from pathlib import Path
from typing import Callable, Dict, Iterator, List, Optional, Tuple
import random
from experimaestro import Config
from datamaestro.definitions import argument, datatasks, Param, Meta
from dataclasses import dataclass
from datamaestro.data import Base, documentation


@dataclass()
class AdhocTopic:
    """The most generic topic: an ID with some text"""

    qid: str
    """Query identifier"""

    text: str
    """The main query text"""

    metadata: Dict[str, str]
    """Extra-information about the query"""


@dataclass(frozen=True)
class AdhocAssessment:
    """Adhoc assessments associate a document ID with a relevance"""

    #: Document identifier
    docno: str

    #: Relevance (> 0 if relevant)
    rel: float


@dataclass()
class AdhocAssessedTopic:
    qid: str
    assessments: List[AdhocAssessment]


@dataclass()
class AdhocDocument:
    """A document with an identifier"""

    docid: str
    text: str
    internal_docid: Optional[int] = None


class AdhocDocuments(Base):
    """A set of documents with identifiers"""

    count: Meta[Optional[int]]
    """Number of documents"""

    def iter(self) -> Iterator[AdhocDocument]:
        """(deprecated, use iter_documents) Returns an iterator over adhoc documents"""
        raise NotImplementedError("No document iterator")

    def iter_documents(self) -> Iterator[AdhocDocument]:
        return self.iter()

    def iter_ids(self) -> Iterator[str]:
        """Iterates over document ids

        By default, use iter_documents, which is not really efficient.
        """
        for doc in self.iter():
            yield doc.docid


class AdhocDocumentStore(AdhocDocuments):
    """A document store

    A document store can
    - match external/internal ID
    - return the document content
    - return the number of documents
    """

    @property
    def documentcount(self):
        """Returns the number of terms in the index"""
        raise NotImplementedError()

    def document_text(self, docid: str) -> str:
        """Returns the text of the document given its id"""
        raise NotImplementedError(f"document_text() for {self.__class__}")

    def docid_internal2external(self, docid: int):
        """Converts an internal collection ID (integer) to an external ID"""
        raise NotImplementedError()

    def document(self, internal_docid: int) -> AdhocDocument:
        """Returns a document given its internal ID"""
        docid = self.docid_internal2external(internal_docid)
        return AdhocDocument(
            docid, self.document_text(docid), internal_docid=internal_docid
        )

    def iter_sample(
        self, randint: Optional[Callable[[int], int]]
    ) -> Iterator[AdhocDocument]:
        """Sample documents from the dataset"""
        length = self.documentcount
        randint = randint or (lambda max: random.randint(0, max - 1))
        while True:
            yield self.document(randint(length))


class AdhocIndex(AdhocDocumentStore):
    """An index can be used to retrieve documents based on terms"""

    @property
    def termcount(self):
        """Returns the number of terms in the index"""
        raise NotImplementedError()

    def term_df(self, term: str):
        """Returns the document frequency"""
        raise NotImplementedError()


class AdhocTopics(Base):
    def iter(self) -> Iterator[AdhocTopic]:
        """Returns an iterator over topics"""
        raise NotImplementedError()

    def count(self) -> Optional[int]:
        """Returns the number of topics if known"""
        return None


class AdhocAssessments(Base):
    """Ad-hoc assessements (qrels)"""

    def iter(self) -> Iterator[AdhocAssessedTopic]:
        """Returns an iterator over assessments"""
        raise NotImplementedError()


class AdhocRun(Base):
    """IR adhoc run"""

    pass


@datatasks("information retrieval")
class Adhoc(Base):
    """An Adhoc IR collection"""

    documents: Param[AdhocDocuments]
    """The set of documents"""

    topics: Param[AdhocTopics]
    """The set of topics"""

    assessments: Param[AdhocAssessments]
    """The set of assessments (for each topic)"""


class RerankAdhoc(Adhoc):
    """Re-ranking ad-hoc task based on an existing run"""

    run: Param[AdhocRun]
    """The run to re-rank"""


class Measure(Config):
    """An Information Retrieval measure"""

    pass


class TrainingTriplets(Base):
    """Triplet for training IR systems: query / query ID, positive document, negative document

    attributes:

        ids: True if the triplet is made of IDs, False otherwise
    """

    ids: Meta[bool]

    def iter(self) -> Iterator[Tuple[str, str, str]]:
        raise NotImplementedError()


def autoopen(path: Path, mode: str):
    print("Reading", path)
    if path.suffix == ".gz":
        import gzip

        return gzip.open(path, mode)
    return path.open(mode)


class TrainingTripletsLines(TrainingTriplets):
    """Training triplets with one line per triple (text only)"""

    sep: Meta[str]
    path: Param[Path]

    def iter(self) -> Iterator[Tuple[str, str, str]]:
        with autoopen(self.path, "rt") as fp:
            for line in fp:
                q, pos, neg = line.strip().split(self.sep)
                yield q, pos, neg
