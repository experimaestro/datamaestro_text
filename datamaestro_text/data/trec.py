from datamaestro.definitions import argument, data
from experimaestro import Any
from datamaestro.data import Base
from pathlib import Path
from .ir import AdhocDocuments, AdhocTopics, AdhocAssessments


@argument("path", type=Path)
@argument("parts", type=Any)
@data()
class TrecTopics(AdhocTopics): pass

@argument("path", type=Path)
@data()
class TrecAssessments(AdhocAssessments): pass

@argument("path", type=Path)
@data()
class TipsterCollection(AdhocDocuments): pass
