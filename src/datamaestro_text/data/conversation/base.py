from abc import ABC, abstractmethod
from enum import Enum
from datamaestro_text.data.ir.base import IDItem, SimpleTextItem
from experimaestro import Param
from typing import Dict, Generic, Iterator, List, Optional, Sequence, Tuple
from attr import define
from datamaestro.record import record_type
from datamaestro.data import Base
from datamaestro.record import Record, Item
from datamaestro_text.data.ir import TopicRecord, Topics
from datamaestro_text.utils.iter import FactoryIterable, LazyList, RangeView

# ---- Basic types


class EntryType(Item, Enum):
    """Type of record"""

    USER_QUERY = 0
    SYSTEM_ANSWER = 1
    CLARIFYING_QUESTION = 2


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


@define
class AnswerEntry(Item):
    """A system answer"""

    answer: str
    """The system answer"""


@define
class AnswerDocumentID(Item):
    """An answer as a document ID"""

    document_id: str


@define
class AnswerDocumentURL(Item):
    """An answer as a document ID"""

    url: str


@define
class RetrievedEntry(Item):
    """List of system-retrieved documents and their relevance"""

    documents: List[str]
    """List of retrieved documents"""

    relevant_documents: Optional[Dict[int, Tuple[Optional[int], Optional[int]]]] = None
    """List of relevance status (optional), with start/stop position"""


@define
class ClarifyingQuestionEntry(Item):
    """A system-generated clarifying question"""

    pass


#: The conversation
ConversationHistory = Sequence[Record]


@define
class ConversationHistoryItem(Item):
    """A user interaction contextualized within a conversation"""

    history: ConversationHistory
    """The history"""


# ---- Abstract conversation representation


class ConversationNode:
    @abstractmethod
    def entry(self) -> Record:
        """The current conversation entry"""
        ...

    @abstractmethod
    def history(self) -> ConversationHistory:
        """Preceding conversation entries, from most recent to more ancient"""
        ...

    @abstractmethod
    def parent(self) -> Optional["ConversationNode"]: ...

    @abstractmethod
    def children(self) -> List["ConversationNode"]: ...


class ConversationTree(ABC):
    """Represents a conversation tree"""

    @abstractmethod
    def root(self) -> ConversationNode: ...

    @abstractmethod
    def __iter__(self) -> Iterator[ConversationNode]:
        """Iterates over conversation nodes"""
        ...


# ---- A conversation tree


class SingleConversationTree(ConversationTree, ABC):
    """Simple conversations, based on a sequence of entries"""

    id: str
    history: List[Record]

    def __init__(self, id: Optional[str], history: List[Record]):
        """Create a simple conversation

        :param history: The entries, in **reverse** order (i.e. more ancient first)
        """
        self.history = history or []
        self.id = id

    def add(self, entry: Record):
        self.history.insert(0, entry)

    def __iter__(self) -> Iterator[ConversationNode]:
        """Iterates over the conversation (starting with the beginning)"""
        for ix in reversed(range(len(self.history))):
            yield SingleConversationTreeNode(self, ix)

    def root(self):
        return SingleConversationTreeNode(self, len(self.history) - 1)


@define
class SingleConversationTreeNode(ConversationNode):
    tree: SingleConversationTree
    index: int

    @property
    def entry(self) -> Record:
        return self.tree.history[self.index]

    @entry.setter
    def entry(self, record: Record):
        try:
            self.tree.history[self.index] = record
        except Exception as e:
            print(e)
            raise

    def history(self) -> Sequence[Record]:
        return self.tree.history[self.index + 1 :]

    def parent(self) -> Optional[ConversationNode]:
        return (
            SingleConversationTreeNode(self.tree, self.index + 1)
            if self.index < len(self.tree.history) - 1
            else None
        )

    def children(self) -> List[ConversationNode]:
        return (
            [SingleConversationTreeNode(self.tree, self.index - 1)]
            if self.index > 0
            else []
        )


class ConversationTreeNode(ConversationNode, ConversationTree):
    """A conversation tree node"""

    entry: Record
    _parent: Optional["ConversationTreeNode"]
    _children: List["ConversationTreeNode"]

    def __init__(self, entry):
        self.entry = entry
        self._parent = None
        self._children = []

    def add(self, node: "ConversationTreeNode") -> "ConversationTreeNode":
        self._children.append(node)
        node._parent = self
        return node

    def conversation(self, skip_self: bool) -> ConversationHistory:
        def iterator():
            current = self.parent() if skip_self else self
            while current is not None:
                yield current.entry
                current = current.parent()

        return LazyList(FactoryIterable(iterator))

    def __iter__(self) -> Iterator["ConversationTreeNode"]:
        """Iterates over all conversation tree nodes (pre-order)"""
        yield self.entry
        for child in self._children:
            yield from child

    def parent(self) -> Optional[ConversationNode]:
        return self._parent

    def children(self) -> List[ConversationNode]:
        return self._children

    def root(self):
        return self


class ConversationDataset(Base, ABC):
    """A dataset made of conversations"""

    @abstractmethod
    def __iter__(self) -> Iterator[ConversationTree]:
        """Return an iterator over conversations"""
        ...


class ConversationDatasetSubset(ConversationDataset):
    """A subset of conversations from another ConversationDataset"""

    original_dataset: Param[ConversationDataset]
    """Optional reference to the original dataset"""

    data_ids: Param[List[int]]
    """IDs of the conversations in the original dataset"""

    def __iter__(self) -> Iterator[ConversationTree]:
        """Return an iterator over the subset of conversations"""
        return iter(list(self.original_dataset)[i] for i in self.data_ids)


def create_conversation_validation_split(
    dataset: ConversationDataset, validation_ratio: float = 0.2, seed: int = 42
) -> Tuple[ConversationDataset, ConversationDataset]:
    """Create train/validation splits from a ConversationDataset

    :param dataset: The original conversation dataset
    :param validation_ratio: Fraction of conversations to use for validation (0.0-1.0)
    :param seed: Random seed for reproducible splits
    :return: Tuple of (train_dataset, validation_dataset)
    """
    import numpy as np

    # Convert generator to list to get all conversations
    all_conversations = list(dataset.__iter__())

    # Shuffle conversations with fixed seed for reproducibility
    rng = np.random.RandomState(seed)
    ids = list(range(len(all_conversations)))
    rng.shuffle(ids)

    # Calculate split point
    split_point = int(len(all_conversations) * (1 - validation_ratio))

    # Create dataset subsets
    train_dataset = ConversationDatasetSubset.C(
        id=dataset.id + "_train", original_dataset=dataset, data_ids=ids[:split_point]
    )
    val_dataset = ConversationDatasetSubset.C(
        id=dataset.id + "_val", original_dataset=dataset, data_ids=ids[split_point:]
    )

    return train_dataset, val_dataset


class ConversationUserTopics(Topics):
    """Extract user topics from conversations"""

    conversations: Param[ConversationDataset]

    topic_recordtype = record_type(IDItem, SimpleTextItem)

    def iter(self) -> Iterator[TopicRecord]:
        """Returns an iterator over topics"""
        for conversation in ConversationDataset:
            raise NotImplementedError()
