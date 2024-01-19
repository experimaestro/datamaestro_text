from attrs import define
from typing import ClassVar, List


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
        return self.id


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


@define(slots=False)
class TextDocument(TextHolder, Document):
    """Documents with text"""


@define(slots=False)
class IDDocument(IDHolder, Document):
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
    pass


@define(slots=False)
class GenericTopic(TextHolder, IDHolder, Topic):
    pass


@define(slots=False)
class TextTopic(TextHolder, Topic):
    pass


@define(slots=False)
class IDTopic(IDHolder, Topic):
    pass


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
