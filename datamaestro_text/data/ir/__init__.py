"""Generic data types for information retrieval"""

from pathlib import Path
from typing import Iterator, Tuple
from datamaestro.definitions import data, argument, datatasks, Param, datatags
from datamaestro.data import Base


@data(description="IR documents")
class AdhocDocuments(Base):
    pass


@data(description="IR topics")
class AdhocTopics(Base):
    def iter(self):
        """Returns an iterator over topics"""
        raise NotImplementedError()


@data(description="IR assessments")
class AdhocAssessments(Base):
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
