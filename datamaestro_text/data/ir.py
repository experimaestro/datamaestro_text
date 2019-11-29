from pathlib import Path
from datamaestro.definitions import Data, Argument

@Data(description="IR documents")
class AdhocDocuments(): pass

@Data(description="IR topics")
class AdhocTopics(): pass

@Data(description="IR assessments")
class AdhocAssessments(): pass

@Argument("documents", type=AdhocDocuments)
@Argument("topics", type=AdhocTopics)
@Argument("assessments", type=AdhocAssessments)
@Data()
class Adhoc(): pass