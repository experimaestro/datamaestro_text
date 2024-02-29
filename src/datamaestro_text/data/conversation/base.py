from abc import ABC, abstractmethod
from typing import Dict, Generic, Iterator, List, Optional, Sequence
from attr import define
from datamaestro.data import Base
from datamaestro.record import Record, Item
from datamaestro_text.data.ir import TopicRecord
from datamaestro_text.utils.iter import FactoryIterable, LazyList, RangeView

# ---- Basic types


class DecontextualizedItem(Item):
    """A topic record with decontextualized versions of the topic"""

    @abstractmethod
    def get_decontextualized_query(self, mode=None) -> str:
        """Returns the decontextualized query"""
        ...


@define
class SimpleDecontextualizedItem(DecontextualizedItem):
    """A topic record with one decontextualized version of the topic"""

    decontextualized_query: str

    @abstractmethod
    def get_decontextualized_query(self, mode=None) -> str:
        """Returns the decontextualized query"""
        assert mode is None

        return self.decontextualized_query


@define
class DecontextualizedDictItem(DecontextualizedItem):
    """A conversation entry providing decontextualized version of the user query"""

    default_decontextualized_key: str

    decontextualized_queries: Dict[str, str]

    def get_decontextualized_query(self, mode=None):
        return self.decontextualized_queries[mode or self.default_decontextualized_key]


class ConversationRecord(Record):
    """A conversation entry"""

    pass


class TopicConversationRecord(ConversationRecord, TopicRecord):
    """A conversation record"""

    pass


class AnswerConversationRecord(ConversationRecord):
    """A conversation record"""

    pass


@define
class AnswerEntry(Item):
    """A system answer"""

    answer: str
    """The system answer"""


@define
class RetrievedEntry(Item):
    """List of system-retrieved documents and their relevance"""

    documents: List[str]
    """List of retrieved documents"""

    document_relevances: Optional[List[str]] = None
    """List of retrieved documents and their relevance status"""


@define
class ClarifyingQuestionEntry(Item):
    """A system-generated clarifying question"""

    pass


#: The conversation
ConversationHistory = Sequence[ConversationRecord]


@define
class ConversationHistoryItem(Item):
    """A user interaction contextualized within a conversation"""

    history: ConversationHistory
    """The history"""


# ---- Abstract conversation representation


class ConversationNode:
    def entry(self) -> ConversationRecord:
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
    history: Sequence[ConversationRecord]

    def __init__(self, id: Optional[str], history: List[ConversationRecord]):
        """Create a simple conversation

        :param history: The entries, in reverse order (i.e. more ancient first)
        """
        self.history = history or []

    def add(self, entry: ConversationRecord):
        self.history.insert(0, entry)

    def __iter__(self) -> Iterator[ConversationNode]:
        for ix in range(len(self.history)):
            yield SingleConversationTreeNode(self, ix)


@define
class SingleConversationTreeNode(ConversationNode):
    tree: SingleConversationTree
    index: int

    def entry(self) -> ConversationRecord:
        return self.tree.history[self.index]

    def history(self) -> Sequence[ConversationRecord]:
        return self.tree.history[self.index + 1 :]


class ConversationTreeNode(ConversationNode, ConversationTree):
    """A conversation tree node"""

    entry: ConversationRecord
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
    def __iter__(self) -> Iterator[ConversationTree]:
        """Return an iterator over conversations"""
        for i in range(len(self)):
            return self.get(i)
