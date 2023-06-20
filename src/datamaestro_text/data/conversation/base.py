from abc import ABC, abstractmethod
from typing import Generic, Iterator, List, Optional, TypeVar, get_origin, get_args
from attr import define
from datamaestro.data import Base


@define(kw_only=True, slots=False)
class Entry:
    query: str
    """The query issued by the user"""


@define(kw_only=True, slots=False)
class DecontextualizedEntry(Entry):
    decontextualized_query: str
    """Human rewritten query"""


@define(kw_only=True, slots=False)
class AnswerEntry(Entry):
    answer: str
    """The system answer"""


@define(kw_only=True, slots=False)
class RetrievedEntry(Entry):
    """List of retrieved documents and their relevance"""

    documents: List[str]
    """List of retrieved documents"""

    document_relevances: Optional[List[str]] = None
    """List of retrieved documents and their relevance status"""


GenericEntry = TypeVar("GenericEntry", bound=Entry)


@define(kw_only=True)
class Conversation(Generic[GenericEntry]):
    id: str
    """The conversation ID"""

    history: List[GenericEntry]
    """The history"""


class ConversationDataset(Base, ABC, Generic[GenericEntry]):
    """A dataset composed of"""

    @classmethod
    def entry_cls(cls, origin=True):
        """Return the generic type class of the entry

        :param origin: if True, return the origin class, otherwise returns a generic type
        """
        hint = next(
            c
            for c in cls.__orig_bases__
            if issubclass(get_origin(c), ConversationDataset)
        )
        arg = get_args(hint)[0]
        return get_origin(arg) if origin else arg

    @abstractmethod
    def iter_conversations(self) -> Iterator[Conversation[Entry]]:
        """Return an iterator over conversations"""
        ...
