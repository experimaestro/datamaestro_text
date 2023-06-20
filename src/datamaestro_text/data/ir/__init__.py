"""Generic data types for information retrieval"""

from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, NamedTuple
import random
from experimaestro import Config
from datamaestro.definitions import datatasks, Param, Meta
from dataclasses import dataclass
from datamaestro.data import Base


AdhocDocument = NamedTuple
AdhocTopic = NamedTuple
AdhocAssessment = NamedTuple


class AdhocDocuments(Base):
    """A set of documents with identifiers

    See `IR Datasets <https://ir-datasets.com/index.html>`_ for the list of query classes
    """

    count: Meta[Optional[int]]
    """Number of documents"""

    def iter(self) -> Iterator:
        """Returns an iterator over documents"""
        raise self.iter_documents()

    def iter_documents(self) -> Iterator[AdhocDocument]:
        return self.iter()

    def iter_ids(self) -> Iterator[str]:
        """Iterates over document ids

        By default, use iter_documents, which is not really efficient.
        """
        for doc in self.iter():
            yield doc.docid

    @property
    def documentcount(self):
        """Returns the number of terms in the index"""
        raise NotImplementedError()


class AdhocDocumentStore(AdhocDocuments):
    """A document store

    A document store can
    - match external/internal ID
    - return the document content
    - return the number of documents
    """

    def docid_internal2external(self, docid: int):
        """Converts an internal collection ID (integer) to an external ID"""
        raise NotImplementedError()

    def document_int(self, internal_docid: int):
        """Returns a document given its internal ID"""
        docid = self.docid_internal2external(internal_docid)
        return self.document(docid)

    def document_ext(self, docid: str):
        """Returns a document given its external ID"""
        raise NotImplementedError(f"document() in {self.__class__}")

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
    """A set of topics with associated IDs

    See `IR Datasets <https://ir-datasets.com/index.html>`_ for the list of query classes
    """

    def iter(self) -> Iterator:
        """Returns an iterator over topics"""
        raise NotImplementedError()

    def count(self) -> Optional[int]:
        """Returns the number of topics if known"""
        return None


class AdhocAssessments(Base):
    """Ad-hoc assessements (qrels)

    See `IR Datasets <https://ir-datasets.com/index.html>`_ for the list of qrels classes
    """

    def iter(self) -> Iterator:
        """Returns an iterator over assessments"""
        raise NotImplementedError()


class AdhocRun(Base):
    """IR adhoc run"""

    pass


class AdhocResults(Base):
    def get_results(self) -> Dict[str, float]:
        """Returns the aggregated results

        :return: Returns a dictionary where each metric (keys) is associated
            with a value
        """
        raise NotImplementedError()


@datatasks("information retrieval")
class Adhoc(Base):
    """An Adhoc IR collection with documents, topics and their assessments"""

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


@dataclass(kw_only=True)
class PairwiseSample:
    """A a query with positive and negative samples"""

    query: str
    """The query (text or ID)"""

    positives: List[str]
    """Relevant documents (text or ID)"""

    negatives: Dict[str, List[str]]
    """Non relevant documents (text or ID), organized in a dictionary where keys
    are the algorithm used to retrieve the negatives"""


class PairwiseSampleDataset(Base):
    """Datasets where each record is a query with positive and negative samples

    attributes:

        ids: True if the triplet is made of IDs, False otherwise
    """

    ids: Meta[bool]
    """Whether data are texts or IDs"""

    def iter(self) -> Iterator[PairwiseSample]:
        raise NotImplementedError()
