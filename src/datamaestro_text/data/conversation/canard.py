from typing import Iterator, List, Optional
from attr import define
import json
from datamaestro.data import File
from .base import Conversation, DecontextualizedEntry
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


@define(kw_only=True, slots=False)
class CanardEntry(DecontextualizedEntry):
    """Entry"""


class CanardDataset(ConversationDataset, File):
    """A dataset in the CANARD json format"""

    def iter(self) -> Iterator[CanardConversation]:
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

    def iter_conversations(self) -> Iterator[Conversation[CanardEntry]]:
        current: Optional[Conversation] = None

        for entry in self.iter():
            # Check if current conversation
            cid = entry.dialogue_id
            if current is None or cid != current.id:
                if current is not None:
                    yield current
                current = Conversation(id=cid, history=[])

            # Add to current
            current.history.append(
                CanardEntry(
                    query=entry.query,
                    decontextualized_query=entry.rewrite,
                )
            )

        yield current
