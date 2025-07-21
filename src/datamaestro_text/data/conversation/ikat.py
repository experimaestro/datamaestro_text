from typing import Iterator, List
from attr import define, field
import json
import logging
from datamaestro.data import File
from datamaestro.record import Record

from datamaestro_text.data.ir import Topics
from datamaestro_text.data.ir.base import (
    IDItem,
    SimpleTextItem,
)


from .base import (
    AnswerEntry,
    ConversationTree,
    EntryType,
    SimpleDecontextualizedItem,
    SingleConversationTree,
)
from . import ConversationDataset

# Keys to change in the dataset entries for compatibility across different years

KEY_MAPPINGS = {
    # Keys to replace: Target Key
    "turns": "responses",
    "utterance": "user_utterance",
    "ptkb_provenance": "relevant_ptkbs",
    "response_provenance": "citations",
}


def norm_dict(entry: dict) -> dict:
    """Convert keys in the entry to match the expected format."""
    normalized = {}
    for k, v in entry.items():
        # Check for direct mapping, then try lowercase mapping
        new_key = KEY_MAPPINGS.get(k) or KEY_MAPPINGS.get(k.lower()) or k.lower()
        normalized[new_key] = v
    return normalized


@define(kw_only=True)
class IkatConversationEntry:
    """A query with past history"""

    turn_id: int
    """Turn number in the conversation"""

    user_utterance: str
    """The last issued query"""

    resolved_utterance: str
    """Manually rewritten query"""

    response: str
    """The system response to the query"""

    relevant_ptkbs: List[str]
    """The list of relevant personal knowledge bases for the query"""

    citations: List[str]
    """The list of citations for the response"""


@define(kw_only=True)
class IkatConversationTopic:
    """A query with past history"""

    number: str
    """Conversation ID"""

    title: str
    """Title of the conversation"""

    ptkb: str
    """The personal knowledge base associated with the user"""

    responses: List[IkatConversationEntry] = field(
        converter=lambda items: [
            IkatConversationEntry(**item) if isinstance(item, dict) else item
            for item in map(norm_dict, items)
        ]
    )
    """The list of responses to the query"""


class IkatConversations(ConversationDataset, File):
    """A dataset containing conversations from the IKAT project"""

    """Keys to change in the dataset entries for compatibility across different years"""

    def entries(self) -> Iterator[IkatConversationTopic]:
        """Reads all conversation entries from the dataset file."""
        with self.path.open("rt") as fp:
            raw_data = json.load(fp)

        logging.debug("Loaded %d entries from %s", len(raw_data), self.path)
        logging.debug(f"raw data has keys {raw_data[0].keys()}")

        for entry in raw_data:
            try:
                normalized_entry = norm_dict(entry)
                yield IkatConversationTopic(**normalized_entry)
            except Exception as e:
                logging.warning(f"Failed to parse entry: {e}")
                raise e

    def __iter__(self) -> Iterator[ConversationTree]:
        for entry in self.entries():
            history: List[Record] = []

            for turn in entry.responses:
                turn: IkatConversationEntry = turn  # Ensure type is correct
                query_id = f"{entry.number}_{turn.turn_id}"

                # USER QUERY record
                history.append(
                    Record(
                        IDItem(query_id),
                        SimpleTextItem(turn.user_utterance),
                        SimpleDecontextualizedItem(turn.resolved_utterance),
                        EntryType.USER_QUERY,
                    )
                )

                # Build citation info (stubbed relevance to match format)
                relevances = {}
                if turn.relevant_ptkbs:
                    # Example: just use first as relevant (can be improved)
                    relevances[0] = (0, None)  # No position info in this structure

                # SYSTEM ANSWER record
                history.append(
                    Record(
                        AnswerEntry(turn.response),
                        EntryType.SYSTEM_ANSWER,
                    )
                )

            # Ensure reverse if needed for compatibility (optional)
            history.reverse()
            yield SingleConversationTree(entry.number, history)
