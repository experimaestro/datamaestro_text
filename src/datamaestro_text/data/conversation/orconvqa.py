from typing import Iterator, List, Optional
from attr import define
import json
from datamaestro.data import File

from .base import (
    AnswerEntry,
    Conversation,
    DecontextualizedEntry,
    RetrievedEntry,
    Conversation,
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


@define(kw_only=True, slots=False)
class OrConvQAEntry(DecontextualizedEntry, RetrievedEntry, AnswerEntry):
    """Entry"""


class OrConvQADataset(ConversationDataset[OrConvQAEntry], File):
    def iter(self) -> Iterator[OrConvQADatasetEntry]:
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

    def iter_conversations(self) -> Iterator[Conversation[OrConvQAEntry]]:
        current: Optional[Conversation] = None

        for entry in self.iter():
            # Check if current conversation
            cid, query_no = entry.query_id.rsplit("#", 1)
            if current is None or cid != current.id:
                if current is not None:
                    yield current
                current = Conversation(id=cid, history=[])

            # Add to current
            current.history.append(
                OrConvQAEntry(
                    query=entry.query,
                    decontextualized_query=entry.rewrite,
                    answer=entry.answer.text,
                    documents=entry.evidences,
                    document_relevances=entry.retrieval_labels,
                )
            )

        yield current
