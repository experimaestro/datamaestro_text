from functools import cached_property
from typing import Iterator, List, Optional
from attr import define
import json
from datamaestro.data import File
from datamaestro.record import Record

from datamaestro_text.data.ir.base import (
    IDItem,
    SimpleTextItem,
)


from .base import (
    AnswerEntry,
    ConversationTree,
    EntryType,
    RetrievedEntry,
    SimpleDecontextualizedItem,
    SingleConversationTree,
)
from . import ConversationDataset


@define(kw_only=True)
class OrConvQADatasetAnswer:
    text: staticmethod
    answer_start: 0
    bid: Optional[int] = None


@define(kw_only=True)
class OrConvQADatasetHistoryEntry:
    question: str
    """The question"""

    answer: OrConvQADatasetAnswer


@define(kw_only=True)
class OrConvQADatasetEntry:
    """A query with past history"""

    query_id: int
    """Question number"""

    query: str
    """The last issued query"""

    rewrite: str
    """Manually rewritten query"""

    history: List[OrConvQADatasetHistoryEntry]
    """The list of queries asked by the user"""

    answer: OrConvQADatasetAnswer

    evidences: List[str]
    """Evidence sources for the conversation"""

    retrieval_labels: List[int]
    """Relevance status for evidences"""


class OrConvQADataset(ConversationDataset, File):
    def entries(self) -> Iterator[OrConvQADatasetEntry]:
        """Iterates over re-written query with their context"""
        with self.path.open("rt") as fp:
            for line in fp.readlines():
                entry = json.loads(line)
                yield OrConvQADatasetEntry(
                    query_id=entry["qid"],
                    query=entry["question"],
                    evidences=entry["evidences"],
                    retrieval_labels=entry["retrieval_labels"],
                    rewrite=entry["rewrite"],
                    answer=OrConvQADatasetAnswer(**entry["answer"]),
                    history=[
                        OrConvQADatasetHistoryEntry(
                            question=history_entry["question"],
                            answer=OrConvQADatasetAnswer(**history_entry["answer"]),
                        )
                        for history_entry in entry["history"]
                    ],
                )

    def __iter__(self) -> Iterator[ConversationTree]:
        history: List[Record] = []
        current_id: Optional[str] = None

        for entry in self.entries():
            # Creates a new conversation if needed
            cid, query_no = entry.query_id.rsplit("#", 1)
            if cid != current_id:
                if current_id is not None:
                    history.reverse()
                    yield SingleConversationTree(current_id, history)

                current_id = cid
                history = []

            # Add to current
            history.append(
                Record(
                    IDItem(entry.query_id),
                    SimpleTextItem(entry.query),
                    SimpleDecontextualizedItem(entry.rewrite),
                    EntryType.USER_QUERY,
                )
            )

            relevances = {}
            for rank, relevance in enumerate(entry.retrieval_labels):
                if relevance > 0:
                    relevances[rank] = (entry.answer.answer_start, None)

            assert (
                len(relevances) <= 1
            ), f"Too many relevance labels ({len(relevances)}) for {entry.query_id}"

            history.append(
                Record(
                    AnswerEntry(entry.answer.text),
                    RetrievedEntry(entry.evidences, relevances),
                    EntryType.SYSTEM_ANSWER,
                )
            )

        # Yields the last one
        history.reverse()
        yield SingleConversationTree(current_id, history)
