from abc import ABC, abstractmethod
from attrs import define
from typing import List
from datamaestro.record import Record, Item, record_type


TopicRecord = DocumentRecord = Record


@define()
class ScoredItem(Item):
    """A score associated with the document"""

    score: float
    """A retrieval score associated with this record (e.g. of the first-stage
    retriever)"""


class TextItem(Item, ABC):
    @property
    @abstractmethod
    def text(self) -> str:
        """Returns the text"""


@define
class SimpleTextItem(TextItem):
    """A topic/document with a text record"""

    text: str


@define
class InternalIDItem(Item, ABC):
    """A topic/document with an internal ID"""

    id: int


@define
class IDItem(Item, ABC):
    """A topic/document with an external ID"""

    id: str


@define
class AdhocAssessment:
    doc_id: str


@define
class SimpleAdhocAssessment(AdhocAssessment):
    rel: float
    """Relevance (> 0 if relevant)"""


@define
class AdhocAssessedTopic:
    topic_id: str
    """The topic ID"""

    assessments: List[AdhocAssessment]
    """List of assessments for this topic"""


def create_record(*items: Item, id: str = None, text: str = None):
    """Easy creation of a text/id item"""
    extra_items = []
    if id is not None:
        extra_items.append(IDItem(id))
    if text is not None:
        extra_items.append(SimpleTextItem(text))
    return Record(*items, *extra_items)
