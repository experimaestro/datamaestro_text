from typing import List, Optional
from datamaestro.definitions import argument, Option
from datamaestro.data import Base
from experimaestro import documentation, Param, Config
from pathlib import Path
from datamaestro_text.data.ir import (
    AdhocDocuments,
    AdhocTopics,
    AdhocAssessments,
    AdhocRun,
    Measure,
)


class TrecAdhocTopics(AdhocTopics):
    path: Option[Path]
    parts: Option[List[str]]

    @documentation
    def iter(self):
        """Iterate over TREC adhoc topics"""
        import datamaestro_text.interfaces.trec as trec

        yield from trec.parse_query_format(self.path)


class TrecAdhocAssessments(AdhocAssessments):
    path: Option[Path]

    def trecpath(self):
        return self.path

    @documentation
    def iter(self):
        """Iterate over TREC adhoc topics"""
        import datamaestro_text.interfaces.trec as trec

        yield from trec.parse_qrels(self.path)


@argument("path", type=Path)
class TrecAdhocRun(AdhocRun):
    pass


class TrecAdhocResults(Base):
    """Adhoc results"""

    metrics: Param[List[Measure]]
    """List of reported metrics"""

    results: Param[Path]
    """Main results"""

    detailed: Param[Optional[Path]]
    """Results per topic (if any)"""


class TipsterCollection(AdhocDocuments):
    path: Param[Path]
