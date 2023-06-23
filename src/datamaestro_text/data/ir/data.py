from attrs import define
from typing import ClassVar, List


class BaseHolder:
    """Base class for topics and documents"""

    has_id: ClassVar[bool] = False
    has_text: ClassVar[bool] = False

    def get_text(self):
        raise RuntimeError(
            f"{type(self)} cannot extract a single text: " "you should use an adapter"
        )

    def get_id(self):
        raise RuntimeError(f"{type(self)} has no ID: " "you should use an adapter")


@define()
class IDHolder:
    """Base data class for ID only data structures"""

    id: str
    has_id: ClassVar[bool] = True

    def get_id(self):
        return self.id


@define()
class TextHolder:
    """Base data class for text only data structures"""

    text: str
    has_text: ClassVar[bool] = True

    def get_text(self):
        return self.text


@define()
class TextAndIDHolder:
    """Base data class for ID and text data structures"""

    id: str
    text: str

    has_id: ClassVar[bool] = True
    has_text: ClassVar[bool] = True

    def get_id(self):
        return self.id

    def get_text(self):
        return self.text


class Document(BaseHolder):
    """Base class for documents"""

    pass


@define()
class TextDocument(TextHolder, Document):
    """Documents with text"""


@define()
class IDDocument(IDHolder, Document):
    """Documents with ID"""


@define()
class GenericDocument(TextAndIDHolder, Document):
    """Documents with ID and text"""


class Topic(BaseHolder):
    pass


@define()
class GenericTopic(TextAndIDHolder, Topic):
    pass


@define()
class TextTopic(TextHolder, Topic):
    pass


@define()
class IDTopic(IDHolder, Topic):
    pass


@define()
class AdhocAssessment:
    doc_id: str


@define()
class SimpleAdhocAssessment(AdhocAssessment):
    rel: float
    """Relevance (> 0 if relevant)"""


@define()
class AdhocAssessedTopic:
    topic_id: str
    """The topic ID"""

    assessments: List[AdhocAssessment]
    """List of assessments for this topic"""
