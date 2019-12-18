from datamaestro.definitions import argument, data
from datamaestro.data import Generic
from pathlib import Path
from .ir import AdhocDocuments, AdhocTopics, AdhocAssessments


@argument("path", type=Path)
@argument("parts")
@data()
class TrecTopics(AdhocTopics): pass

@argument("path", type=Path)
@data()
class TrecAssessments(AdhocAssessments): pass

@argument("path", type=Path)
@data()
class TipsterCollection(AdhocDocuments): pass
