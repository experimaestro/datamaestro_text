"""Generic data types for information retrieval"""

from pathlib import Path
from typing import Iterator, NamedTuple, Optional, Tuple
from datamaestro.definitions import data, argument, datatasks, Param, Option
from datamaestro.data import Base, documentation


class AdhocTopic(NamedTuple):
    """Standard topic with an ID, title (keyword query), description (long query) and narrative"""

    qid: str
    title: str
    description: str
    narrative: str


class AdhocDocument:
    """A document with an identifier"""

    docid: str
    text: str

    def __init__(self, docid: str, text: str):
        self.docid = docid
        self.text = text


@data(description="IR documents")
class AdhocDocuments(Base):
    """A set of documents with identifiers"""

    # Number of documents
    count: Option[Optional[int]]

    @documentation
    def iter(self) -> Iterator[AdhocDocument]:
        """Returns an iterator over adhoc documents"""
        raise NotImplementedError("No document iterator")


@data(description="IR topics")
class AdhocTopics(Base):
    def iter(self) -> Iterator[AdhocTopic]:
        """Returns an iterator over topics"""
        raise NotImplementedError()


@data(description="IR assessments")
class AdhocAssessments(Base):
    """Ad-hoc assessements (qrels)"""

    def iter(self):
        """Returns an iterator over assessments"""
        raise NotImplementedError()


@data(description="IR adhoc run")
class AdhocRun(Base):
    pass


@datatasks("information retrieval")
@data()
class Adhoc(Base):
    """An Adhoc IR collection"""

    documents: Param[AdhocDocuments]
    topics: Param[AdhocTopics]
    assessments: Param[AdhocAssessments]


@argument("run", type=AdhocRun)
@data(description="Re-ranking task")
class RerankAdhoc(Adhoc):
    """Re-ranking ad-hoc task"""

    pass


@argument(
    "ids", type=bool, help="Wether the triplet is made of ids (for the documents)"
)
@data(
    description="Triplet for training IR systems: query / query ID, positive document, negative document"
)
class TrainingTriplets(Base):
    def iter(self) -> Iterator[Tuple[str, str, str]]:
        raise NotImplementedError()


class TrainingTripletsLines(TrainingTriplets):
    """Training triplets with one line per triple
    """

    path: Param[Path]
