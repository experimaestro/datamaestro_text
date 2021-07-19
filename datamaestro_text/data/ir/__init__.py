"""Generic data types for information retrieval"""

from pathlib import Path
from typing import Iterator, List, Optional, Tuple
from datamaestro.definitions import argument, datatasks, Param, Meta
from dataclasses import dataclass
from datamaestro.data import Base, documentation


@dataclass()
class AdhocTopic:
    """The most generic topic: an ID with some text"""

    qid: str
    text: str


@dataclass()
class AdhocAssessment:
    """Adhoc assessments associate a document ID with a relevance"""

    docno: str
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


class AdhocDocuments(Base):
    """A set of documents with identifiers

    Attributes:

    count: number of documents or passages
    """

    count: Meta[Optional[int]]

    @documentation
    def iter(self) -> Iterator[AdhocDocument]:
        """Returns an iterator over adhoc documents"""
        raise NotImplementedError("No document iterator")


class AdhocTopics(Base):
    def iter(self) -> Iterator[AdhocTopic]:
        """Returns an iterator over topics"""
        raise NotImplementedError()


class AdhocAssessments(Base):
    """Ad-hoc assessements (qrels)"""

    def iter(self) -> Iterator[AdhocAssessment]:
        """Returns an iterator over assessments"""
        raise NotImplementedError()


class AdhocRun(Base):
    """IR adhoc run"""

    pass


@datatasks("information retrieval")
class Adhoc(Base):
    """An Adhoc IR collection"""

    documents: Param[AdhocDocuments]
    topics: Param[AdhocTopics]
    assessments: Param[AdhocAssessments]


@argument("run", type=AdhocRun)
class RerankAdhoc(Adhoc):
    """Re-ranking ad-hoc task based on an existing run"""

    pass


class TrainingTriplets(Base):
    """Triplet for training IR systems: query / query ID, positive document, negative document

    attributes:

    ids: True if the triplet is made of IDs, False otherwise
    """

    ids: Meta[bool]

    def iter(self) -> Iterator[Tuple[str, str, str]]:
        raise NotImplementedError()


class TrainingTripletsLines(TrainingTriplets):
    """Training triplets with one line per triple (text only)
    """

    path: Param[Path]
