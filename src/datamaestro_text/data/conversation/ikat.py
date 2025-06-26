from typing import Iterator, List, Optional
from attr import define, field
import json
import logging
from datamaestro.data import File
from datamaestro.record import Record

from datamaestro_text.data.ir.base import (
    IDItem,
    SimpleTextItem,
)


from .base import (
    AnswerDocumentURL,
    AnswerEntry,
    ConversationTree,
    EntryType,
    SimpleDecontextualizedItem,
    SingleConversationTree,
)
from . import ConversationDataset



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
class IkatDatasetEntry:
    """A query with past history"""

    number: str
    """Conversation ID"""

    title: str
    """Title of the conversation"""

    ptkb: str
    """The personal knowledge base associated with the user"""

    responses: List[IkatConversationEntry] = field(
        converter=lambda items: [IkatConversationEntry(**item) if isinstance(item, dict) else item for item in items]
    )
    """The list of responses to the query"""


class IkatDataset(ConversationDataset, File):

    def entries(self) -> Iterator[IkatDatasetEntry]:
        """Reads all conversation entries from the dataset file."""
        with self.path.open("rt") as fp:
            raw_data = json.load(fp)

        logging.debug("Loaded %d entries from %s", len(raw_data), self.path)
        logging.debug(f"raw data has keys {raw_data[0].keys()}")

        processed_data = []
        for entry in raw_data:
            processed_data.append(IkatDatasetEntry(**{key.lower(): value for key, value in entry.items()}))

        logging.debug(f"First parsed data sample: {processed_data[0]}")
        return iter(processed_data)

    def __iter__(self) -> Iterator[ConversationTree]:
        for entry in self.entries():
            history: List[Record] = []

            for turn in entry.responses:
                turn: IkatConversationEntry = turn  # Ensure type is correct
                query_id = f"{entry.number}#{turn.turn_id}"

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

