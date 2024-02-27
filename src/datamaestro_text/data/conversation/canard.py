from typing import Iterator, List, Optional
from attr import define
import json
from datamaestro.data import File
from datamaestro.record import recordtypes
from datamaestro_text.data.ir.base import GenericTopicRecord
from .base import (
    AnswerEntry,
    ConversationTree,
    RetrievedEntry,
    SingleConversationTree,
    SimpleDecontextualizedItem,
    AnswerConversationRecord,
)
from . import ConversationDataset


@define(kw_only=True)
class CanardConversation:
    """A query with past history"""

    history: List[str]
    """The list of queries asked by the user"""

    query: str
    """The last issued query"""

    rewrite: str
    """Manually rewritten query"""

    dialogue_id: str
    """Conversation identifier"""

    query_no: int
    """Question number"""


@recordtypes(SimpleDecontextualizedItem)
class CanardTopicRecord(GenericTopicRecord):
    pass


@recordtypes(AnswerEntry, RetrievedEntry)
class CanardAnswerRecord(AnswerConversationRecord):
    pass


class CanardDataset(ConversationDataset, File):
    """A dataset in the CANARD JSON format"""

    def entries(self) -> Iterator[CanardConversation]:
        """Iterates over re-written query with their context"""
        with self.path.open("rt") as fp:
            data = json.load(fp)

        for entry in data:
            yield CanardConversation(
                history=entry["History"],
                query=entry["Question"],
                rewrite=entry["Rewrite"],
                dialogue_id=entry["QuAC_dialog_id"],
                query_no=entry["Question_no"],
            )

    def __iter__(self) -> Iterator[ConversationTree]:
        history = []
        current_id = None

        for entry in self.entries():
            # Check if current conversation
            if current_id != entry.dialogue_id and current_id is not None:
                history.reverse()
                yield SingleConversationTree(current_id, history)

            # Add to current
            history.append(
                # FIXME: not working anymore
                CanardEntry(
                    query=entry.query,
                    decontextualized_query=entry.rewrite,
                )
            )

        yield current
