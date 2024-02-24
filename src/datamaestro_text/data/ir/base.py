from attrs import define
from typing import ClassVar, Generic, List, TypeVar


class BaseHolder:
    """Base class for topics and documents"""

    has_id: ClassVar[bool] = False
    has_internal_id: ClassVar[bool] = False
    has_text: ClassVar[bool] = False

    def get_text(self):
        raise RuntimeError(
            f"{type(self)} cannot extract a single text: " "you should use an adapter"
        )

    def get_id(self) -> str:
        raise RuntimeError(f"{type(self)} has no ID: " "you should use an adapter")

    def get_internal_id(self) -> int:
        raise RuntimeError(
            f"{type(self)} has no internal ID: " "you should use an adapter"
        )


@define(slots=False)
class IDHolder(BaseHolder):
    """Base data class for ID only data structures"""

    id: str
    has_id: ClassVar[bool] = True

    def get_id(self):
        return self.id


@define(slots=False)
class InternalIDHolder(BaseHolder):
    """Base data class for ID only data structures"""

    internal_id: int
    has_internal_id: ClassVar[bool] = True

    def get_internal_id(self) -> int:
        return self.internal_id


@define(slots=False)
class TextHolder(BaseHolder):
    """Base data class for text only data structures"""

    text: str
    has_text: ClassVar[bool] = True

    def get_text(self):
        return self.text


class Document(BaseHolder):
    """Base class for documents"""

    pass


DocumentType = TypeVar("DocumentType", bound=Document)


@define
class DocumentRecord(Generic[DocumentType]):
    document: DocumentType

    @staticmethod
    def from_text(text: str) -> "DocumentRecord[TextDocument]":
        return DocumentRecord(TextDocument(text))


@define()
class ScoredDocumentRecord(DocumentRecord[DocumentType]):
    """A document record when training models"""

    score: float
    """A retrieval score associated with this record (e.g. of the first-stage
    retriever)"""


@define(slots=False)
class TextDocument(TextHolder, Document):
    """Documents with text"""


@define(slots=False)
class IDDocument(IDHolder, Document):
    """Documents with ID"""


@define(slots=False)
class InternalIDDocument(InternalIDHolder, Document):
    """Documents with ID"""


@define(slots=False)
class FullIDDocument(InternalIDHolder, IDHolder, Document):
    """Documents with internal and external ID"""


@define(slots=False)
class GenericDocument(TextHolder, IDHolder, Document):
    """Documents with ID and text"""


@define(slots=False)
class FullGenericDocument(TextHolder, IDHolder, InternalIDHolder, Document):
    """Documents with ID and text"""


class Topic(BaseHolder):
    def as_record(self):
        return TopicRecord(self)


@define(slots=False)
class GenericTopic(TextHolder, IDHolder, Topic):
    pass


@define(slots=False)
class TextTopic(TextHolder, Topic):
    pass


@define(slots=False)
class IDTopic(IDHolder, Topic):
    pass


TopicType = TypeVar("TopicType", bound=Topic)


@define(slots=False)
class TopicRecord(Generic[TopicType]):
    topic: TopicType

    @staticmethod
    def from_text(text: str) -> "TopicRecord[TextDocument]":
        return TopicRecord(TextDocument(text))

    def as_record(self):
        return self


@define(slots=False)
class AdhocAssessment:
    doc_id: str


@define(slots=False)
class SimpleAdhocAssessment(AdhocAssessment):
    rel: float
    """Relevance (> 0 if relevant)"""


@define(slots=False)
class AdhocAssessedTopic:
    topic_id: str
    """The topic ID"""

    assessments: List[AdhocAssessment]
    """List of assessments for this topic"""
