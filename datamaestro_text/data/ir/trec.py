from typing import List
from datamaestro.definitions import argument, data, Option
from experimaestro import documentation
from pathlib import Path
from datamaestro_text.data.ir import (
    AdhocDocuments,
    AdhocTopics,
    AdhocAssessments,
    AdhocRun,
)


@data()
class TrecAdhocTopics(AdhocTopics):
    path: Option[Path]
    parts: Option[List[str]]

    @documentation
    def iter(self):
        """Iterate over TREC adhoc topics"""
        import datamaestro_text.interfaces.trec as trec

        yield from trec.parse_query_format(self.path)


@data()
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
@data()
class TrecAdhocRun(AdhocRun):
    pass


@argument(
    "metrics",
    required=False,
    type=List[str],
    help="List of reported metrics (None if all from trec_eval)",
)
@argument("results", type=Path, help="Main results")
@argument("detailed", type=Path, required=False, help="Results per topic (if any)")
@data()
class TrecAdhocResults:
    pass


@argument("path", type=Path)
@data()
class TipsterCollection(AdhocDocuments):
    pass
