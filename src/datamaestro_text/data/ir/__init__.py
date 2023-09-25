"""Generic data types for information retrieval"""

from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
from attrs import define
from typing import Callable, Dict, Iterator, List, Optional, Tuple, Type
import random
from experimaestro import Config
from datamaestro.definitions import datatasks, Param, Meta
from dataclasses import dataclass
from datamaestro.data import Base
from datamaestro_text.utils.files import auto_open
from .base import (
    Document,
    Topic,
    AdhocAssessment,
    IDTopic,
    IDDocument,
    TextTopic,
    TextDocument,
)


class Documents(Base):
    """A set of documents with identifiers

    See `IR Datasets <https://ir-datasets.com/index.html>`_ for the list of query classes
    """

    count: Meta[Optional[int]]
    """Number of documents"""

    def iter(self) -> Iterator[Document]:
        """Returns an iterator over documents"""
        raise self.iter_documents()

    def iter_documents(self) -> Iterator[Document]:
        return self.iter()

    def iter_ids(self) -> Iterator[str]:
        """Iterates over document ids

        By default, use iter_documents, which is not really efficient.
        """
        for doc in self.iter():
            yield doc.get_id()

    @property
    def documentcount(self):
        """Returns the number of terms in the index"""
        if self.count is not None:
            return self.count

        raise NotImplementedError(f"For class {self.__class__}")

    @property
    def document_cls(self) -> Type[Document]:
        """The class for documents"""
        raise NotImplementedError(f"For class {self.__class__}")


class DocumentStore(Documents):
    """A document store

    A document store can
    - match external/internal ID
    - return the document content
    - return the number of documents
    """

    def docid_internal2external(self, docid: int):
        """Converts an internal collection ID (integer) to an external ID"""
        raise NotImplementedError(f"For class {self.__class__}")

    def document_int(self, internal_docid: int) -> Document:
        """Returns a document given its internal ID"""
        docid = self.docid_internal2external(internal_docid)
        return self.document(docid)

    def document_ext(self, docid: str) -> Document:
        """Returns a document given its external ID"""
        raise NotImplementedError(f"document() in {self.__class__}")

    def documents_ext(self, docids: List[str]) -> Document:
        """Returns documents given their external ID

        By default, just look using `document_ext`, but some store might
        optimize batch retrieval
        """
        return [self.document_ext(docid) for docid in docids]

    def iter_sample(
        self, randint: Optional[Callable[[int], int]]
    ) -> Iterator[Document]:
        """Sample documents from the dataset"""
        length = self.count()
        randint = randint or (lambda max: random.randint(0, max - 1))
        while True:
            yield self.document_int(randint(length))


class AdhocIndex(DocumentStore):
    """An index can be used to retrieve documents based on terms"""

    @property
    def termcount(self):
        """Returns the number of terms in the index"""
        raise NotImplementedError(f"For class {self.__class__}")

    def term_df(self, term: str):
        """Returns the document frequency"""
        raise NotImplementedError(f"For class {self.__class__}")


class Topics(Base):
    """A set of topics with associated IDs"""

    def iter(self) -> Iterator[Topic]:
        """Returns an iterator over topics"""
        raise NotImplementedError(f"For class {self.__class__}")

    def count(self) -> Optional[int]:
        """Returns the number of topics if known"""
        return None

    @property
    def topic_cls(self) -> Type[Topic]:
        """The class for topics"""
        raise NotImplementedError(f"For class {self.__class__}")


AdhocTopics = Topics


class TopicsStore(Topics):
    """Adhoc topics store"""

    @abstractmethod
    def topic_int(self, internal_topic_id: int) -> Topic:
        """Returns a document given its internal ID"""

    @abstractmethod
    def topic_ext(self, external_topic_id: int) -> Topic:
        """Returns a document given its external ID"""


class AdhocAssessments(Base, ABC):
    """Ad-hoc assessments (qrels)"""

    def iter(self) -> Iterator[AdhocAssessment]:
        """Returns an iterator over assessments"""
        raise NotImplementedError(f"For class {self.__class__}")


class AdhocRun(Base):
    """IR adhoc run"""

    pass


class AdhocResults(Base):
    def get_results(self) -> Dict[str, float]:
        """Returns the aggregated results

        :return: Returns a dictionary where each metric (keys) is associated
            with a value
        """
        raise NotImplementedError(f"For class {self.__class__}")


@datatasks("information retrieval")
class Adhoc(Base):
    """An Adhoc IR collection with documents, topics and their assessments"""

    documents: Param[Documents]
    """The set of documents"""

    topics: Param[Topics]
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
    """Triplet for training IR systems: query / query ID, positive document,
    negative document"""

    def iter(self) -> Iterator[Tuple[Topic, Document, Document]]:
        raise NotImplementedError(f"For class {self.__class__}")

    def count(self):
        """Returns the number of triplets or None"""
        return None

    @property
    def topic_cls(self) -> Type[Topic]:
        """The class for topics"""
        raise NotImplementedError(f"For class {self.__class__}")

    @property
    def document_cls(self) -> Type[Document]:
        """The class for documents"""
        raise NotImplementedError(f"For class {self.__class__}")


class TrainingTripletsLines(TrainingTriplets):
    """Training triplets with one line per triple (query texts)"""

    sep: Meta[str]
    path: Param[Path]

    doc_ids: Meta[bool]
    """True if we have documents IDs"""

    topic_ids: Meta[bool]
    """True if we have query IDs"""

    def iter(self) -> Iterator[Tuple[Topic, Document, Document]]:
        with auto_open(self.path, "rt") as fp:
            for line in fp:
                q, pos, neg = line.strip().split(self.sep)
                yield self.topic_cls(q), self.document_cls(pos), self.document_cls(neg)

    @cached_property
    def topic_cls(self) -> Type[Topic]:
        """The class for topics"""
        return IDTopic if self.topic_ids else TextTopic

    @cached_property
    def document_cls(self) -> Type[Document]:
        """The class for documents"""
        return IDDocument if self.doc_ids else TextDocument


@define(kw_only=True)
class PairwiseSample:
    """A a query with positive and negative samples"""

    topic: Topic
    """The topic"""

    positives: List[Document]
    """Relevant documents"""

    negatives: Dict[str, List[Document]]
    """Non relevant documents, organized in a dictionary where keys
    are the algorithm used to retrieve the negatives"""

    @property
    def topic_cls(self):
        """The class for topics"""
        raise NotImplementedError(f"For class {self.__class__}")

    @property
    def document_cls(self):
        """The class for documents"""
        raise NotImplementedError(f"For class {self.__class__}")


class PairwiseSampleDataset(Base):
    """Datasets where each record is a query with positive and negative samples"""

    def iter(self) -> Iterator[PairwiseSample]:
        raise NotImplementedError(f"For class {self.__class__}")
