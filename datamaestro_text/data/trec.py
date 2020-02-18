from datamaestro.definitions import argument, data
from experimaestro import Any
from datamaestro.data import Base
from pathlib import Path
from .ir import AdhocDocuments, AdhocTopics, AdhocAssessments, AdhocResults


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
class TrecAdhocResults(AdhocResults):
    pass


# --- Document collections


@argument("path", type=Path)
@data()
class TipsterCollection(AdhocDocuments):
    pass
