from datamaestro.definitions import Argument, Data
from datamaestro.data import Generic
from pathlib import Path
from .ir import AdhocDocuments, AdhocTopics, AdhocAssessments


@Argument("path", type=Path)
@Data()
class TrecTopics(AdhocTopics): pass

@Argument("path", type=Path)
@Data()
class TrecAssessments(AdhocAssessments): pass

@Argument("path", type=Path)
@Data()
class TipsterCollection(AdhocDocuments): pass
