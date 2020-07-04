from typing import List
from datamaestro.definitions import argument, data
from experimaestro import Any
from datamaestro.data import Base
from pathlib import Path
from datamaestro_text.data.ir import AdhocDocuments, AdhocTopics, AdhocAssessments, AdhocRun


@argument("path", type=Path)
@argument("parts", type=Any)
@data()
class TrecAdhocTopics(AdhocTopics):
    pass


@argument("path", type=Path)
@data()
class TrecAdhocAssessments(AdhocAssessments):
    pass


@argument("path", type=Path)
@data()
class TrecAdhocRun(AdhocRun):
    pass

@argument("metrics", required=False, type=List[str], help="List of reported metrics (None if all from trec_eval)")
@argument("results", type=Path, help="Main results")
@argument("detailed", type=Path, required=False, help="Results per topic (if any)")
@data()
class TrecAdhocResults():
    pass


@argument("path", type=Path)
@data()
class TipsterCollection(AdhocDocuments):
    pass
