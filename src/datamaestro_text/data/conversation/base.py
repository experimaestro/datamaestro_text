from abc import ABC, abstractmethod
from typing import Dict, Generic, Iterator, List, Optional, Sequence
from attr import define
from datamaestro.data import Base

from datamaestro_text.data.ir.base import TopicRecord, TopicType
from datamaestro_text.utils.iter import FactoryIterable, LazyList, RangeView

# ---- Basic types


@define(slots=False)
class DecontextualizedRecord:
    """A topic record with decontextualized versions of the topic"""

    @abstractmethod
    def get_decontextualized_query(self, mode=None) -> str:
        """Returns the decontextualized query"""
        ...


@define(slots=False)
class SimpleDecontextualizedRecord:
    """A topic record with one decontextualized version of the topic"""

    decontextualized_query: str

    @abstractmethod
    def get_decontextualized_query(self, mode=None) -> str:
        """Returns the decontextualized query"""
        assert mode is None

        return self.decontextualized_query


@define(slots=False)
class DecontextualizedDictRecord:
    """A conversation entry providing decontextualized version of the user query"""

    default_decontextualized_key: str

    decontextualized_queries: Dict[str, str]

    def get_decontextualized_query(self, mode=None):
        return self.decontextualized_queries[mode or self.default_decontextualized_key]


class ConversationEntry:
    """A conversation entry"""

    pass


@define(slots=False)
class AnswerEntry(ConversationEntry):
    """A system answer"""

    answer: str
    """The system answer"""


@define(slots=False)
class RetrievedEntry(ConversationEntry):
    """List of system-retrieved documents and their relevance"""

    documents: List[str]
    """List of retrieved documents"""

    document_relevances: Optional[List[str]] = None
    """List of retrieved documents and their relevance status"""


@define(slots=False)
class ClarifyingQuestionEntry(ConversationEntry):
    """A system-generated clarifying question"""

    pass


#: The conversation
ConversationHistory = Sequence[ConversationEntry]


@define
class ConversationTopicRecord(Generic[TopicType]):
    """A user interaction contextualized within a conversation"""

    record: TopicRecord[TopicType]
    """The record"""

    history: ConversationHistory
    """The history"""


# ---- Abstract conversation representation


class ConversationNode:
    def entry(self) -> ConversationEntry:
        """The current conversation entry"""
        ...

    def history(self) -> ConversationHistory:
        """Preceding conversation entries, from most recent to more ancient"""
        ...


class ConversationTree:
    def __iter__(self) -> Iterator[ConversationNode]:
        """Iterates over conversation nodes"""
        pass


# ---- A conversation tree


class SingleConversationTree(ConversationTree):
    """Simple conversations, based on a sequence of entries"""

    id: str
    history: Sequence[ConversationEntry]

    def __init__(self, id: Optional[str], history: List[ConversationEntry]):
        """Create a simple conversation

        :param history: The entries, in reverse order (i.e. more ancient first)
        """
        self.history = history or []

    def add(self, entry: ConversationEntry):
        self.history.insert(0, entry)

    def __iter__(self) -> Iterator[ConversationNode]:
        for ix in range(len(self.history)):
            yield SingleConversationTreeNode(self, ix)


@define
class SingleConversationTreeNode(ConversationNode):
    tree: SingleConversationTree
    index: int

    def entry(self) -> ConversationEntry:
        return self.tree.history[self.index]

    def history(self) -> Sequence[ConversationEntry]:
        return self.tree.history[self.index + 1 :]


class ConversationTreeNode(ConversationNode, ConversationTree):
    """A conversation tree node"""

    entry: ConversationEntry
    parent: Optional["ConversationTreeNode"]
    children: List["ConversationTreeNode"]

    def __init__(self, entry):
        self.entry = entry
        self.parent = None
        self.children = []

    def add(self, node: "ConversationTreeNode") -> "ConversationTreeNode":
        self.children.append(node)
        node.parent = self
        return node

    def conversation(self, skip_self: bool) -> ConversationHistory:
        def iterator():
            current = self.parent if skip_self else self
            while current is not None:
                yield current.entry
                current = current.parent

        return LazyList(FactoryIterable(iterator))

    def __iter__(self) -> Iterator["ConversationTreeNode"]:
        """Iterates over all conversation tree nodes (pre-order)"""
        yield self.entry
        for child in self.children:
            yield from child


class ConversationDataset(Base, ABC):
    """A dataset made of conversations"""

    @abstractmethod
    def get(self, key: int):
        """Return an iterator over conversations"""
        ...

    @abstractmethod
    def __len__(self) -> int:
        """Returns the number of conversation trees"""
        ...

    def __iter__(self) -> Iterator[ConversationTree]:
        """Return an iterator over conversations"""
        for i in range(len(self)):
            return self.get(i)

    def __getitem__(self, key):
        """Return an iterator over conversations"""
        if isinstance(key, int):
            return self.get(key)

        return RangeView(self, key)
