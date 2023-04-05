from typing import Iterator, List
from attr import define
import json
from datamaestro.data import Base, File


@define(kw_only=True)
class ContextualizedRewrittenQuery:
    """A contextualized query"""

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


class ContextualizedQueryRewriting(Base):
    """A dataset composed of"""

    def iter(self) -> Iterator[ContextualizedRewrittenQuery]:
        raise NotImplementedError


class CanardDataset(ContextualizedQueryRewriting, File):
    """A dataset in the CANARD json format"""

    def iter(self) -> Iterator[ContextualizedRewrittenQuery]:
        """Iterates over re-written query with their context"""
        with self.path.open("rt") as fp:
            data = json.load(fp)

        for entry in data:
            yield ContextualizedRewrittenQuery(
                history=entry["History"],
                query=entry["Question"],
                rewrite=entry["Rewrite"],
                dialogue_id=entry["QuAC_dialog_id"],
                query_no=entry["Question_no"],
            )
