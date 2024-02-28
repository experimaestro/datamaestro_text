"""Generic data types for information retrieval"""

from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
from attrs import define
from typing import Callable, Dict, Iterator, List, Optional, Tuple, Type
import random
from experimaestro import Config
from datamaestro.definitions import datatasks, Param, Meta
from datamaestro.data import Base
from datamaestro_text.utils.files import auto_open
from datamaestro_text.utils.iter import BatchIterator
from datamaestro.record import Record
from .base import (  # noqa: F401
    # Record items
    IDItem,
    TextItem,
    InternalIDItem,
    TopicRecord,
    DocumentRecord,
    SimpleTextItem,
    ScoredItem,
    # Pre-defined usual records
    GenericTopicRecord,
    GenericDocumentRecord,
    IDTopicRecord,
    IDDocumentRecord,
    SimpleTextTopicRecord,
    SimpleTextDocumentRecord,
    # Other things
    AdhocAssessment,
)


class Documents(Base):
    """A set of documents with identifiers

    See `IR Datasets <https://ir-datasets.com/index.html>`_ for the list of query classes
    """

    count: Meta[Optional[int]]
    """Number of documents"""

    def iter(self) -> Iterator[DocumentRecord]:
        """Returns an iterator over documents"""
        raise self.iter_documents()

    def iter_documents(self) -> Iterator[DocumentRecord]:
        return self.iter()

    def iter_ids(self) -> Iterator[str]:
        """Iterates over document ids

        By default, use iter_documents, which is not really efficient.
        """
        for doc in self.iter():
            yield doc[IDItem].id

    @property
    def documentcount(self):
        """Returns the number of terms in the index"""
        if self.count is not None:
            return self.count

        raise NotImplementedError(f"For class {self.__class__}")

    @property
    @abstractmethod
    def document_recordtype(self) -> Type[DocumentRecord]:
        """The class for documents"""
        ...


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

    def document_int(self, internal_docid: int) -> DocumentRecord:
        """Returns a document given its internal ID"""
        docid = self.docid_internal2external(internal_docid)
        return self.document(docid)

    def document_ext(self, docid: str) -> DocumentRecord:
        """Returns a document given its external ID"""
        raise NotImplementedError(f"document() in {self.__class__}")

    def documents_ext(self, docids: List[str]) -> List[DocumentRecord]:
        """Returns documents given their external ID

        By default, just look using `document_ext`, but some store might
        optimize batch retrieval
        """
        return [self.document_ext(docid) for docid in docids]

    def iter_sample(
        self, randint: Optional[Callable[[int], int]]
    ) -> Iterator[DocumentRecord]:
        """Sample documents from the dataset"""
        length = self.documentcount
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


class Topics(Base, ABC):
    """A set of topics with associated IDs"""

    @abstractmethod
    def iter(self) -> Iterator[TopicRecord]:
        """Returns an iterator over topics"""
        ...

    def __iter__(self):
        return self.iter()

    def count(self) -> Optional[int]:
        """Returns the number of topics if known"""
        return None

    @property
    @abstractmethod
    def topic_recordtype(self) -> Type[TopicRecord]:
        """The class for topics"""


AdhocTopics = Topics


class TopicsStore(Topics):
    """Adhoc topics store"""

    @abstractmethod
    def topic_int(self, internal_topic_id: int) -> TopicRecord:
        """Returns a document given its internal ID"""

    @abstractmethod
    def topic_ext(self, external_topic_id: int) -> TopicRecord:
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


Triplets = Tuple[TopicRecord, DocumentRecord, DocumentRecord]


class TrainingTriplets(Base, ABC):
    """Triplet for training IR systems: query / query ID, positive document,
    negative document"""

    def iter(self) -> Iterator[Triplets]:
        """Returns an iterator over (topic, document 1, document) triplets"""
        raise NotImplementedError(f"For class {self.__class__}")

    def batch_iter(self, size: int) -> Iterator[List[Triplets]]:
        """Returns an iterator over batches of triplets

        The default implementation just concatenates triplets using `iter`, but
        some classes might use more efficient ways to provide batches of data
        """
        return BatchIterator(self.iter(), size)

    def count(self):
        """Returns the number of triplets or None"""
        return None

    @property
    @abstractmethod
    def topic_recordtype(self) -> Type[Record]:
        """The set of records for topics"""
        ...

    @property
    @abstractmethod
    def document_recordtype(self) -> Type[Record]:
        """The class for documents"""
        ...


class TrainingTripletsLines(TrainingTriplets):
    """Training triplets with one line per triple (query texts)"""

    sep: Meta[str]
    path: Param[Path]

    doc_ids: Meta[bool]
    """True if we have documents IDs"""

    topic_ids: Meta[bool]
    """True if we have query IDs"""

    def iter(self) -> Iterator[Triplets]:
        with auto_open(self.path, "rt") as fp:
            for line in fp:
                q, pos, neg = line.strip().split(self.sep)
                yield self._topic(q), self._doc(pos), self._doc(neg)

    @cached_property
    def _doc(self):
        return lambda doc: self.document_recordtype(
            IDItem(doc) if self.doc_ids else SimpleTextItem(doc)
        )

    @cached_property
    def _topic(self):
        return lambda q: self.topic_recordtype(
            IDItem(q) if self.topic_ids else SimpleTextItem(q)
        )

    @cached_property
    def topic_recordtype(self) -> Type[TopicRecord]:
        """The class for topics"""
        return IDTopicRecord if self.topic_ids else SimpleTextTopicRecord

    @cached_property
    def document_recordtype(self) -> Type[DocumentRecord]:
        """The class for documents"""
        return IDDocumentRecord if self.doc_ids else SimpleTextDocumentRecord


@define(kw_only=True)
class PairwiseSample(ABC):
    """A a query with positive and negative samples"""

    topics: List[TopicRecord]
    """The topic(s)"""

    positives: List[DocumentRecord]
    """Relevant documents"""

    negatives: Dict[str, List[DocumentRecord]]
    """Non relevant documents, organized in a dictionary where keys
    are the algorithm used to retrieve the negatives"""

    @property
    @abstractmethod
    def topic_recordtype(self) -> Type[DocumentRecord]:
        """The class for topics"""

    @property
    @abstractmethod
    def document_recordtype(self) -> Type[DocumentRecord]:
        """The class for documents"""


class PairwiseSampleDataset(Base, ABC):
    """Datasets where each record is a query with positive and negative samples"""

    @abstractmethod
    def iter(self) -> Iterator[PairwiseSample]:
        ...
