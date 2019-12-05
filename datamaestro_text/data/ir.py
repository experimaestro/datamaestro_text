from pathlib import Path
from datamaestro.definitions import Data, Argument, DataTasks, DataTags

@Data(description="IR documents")
class AdhocDocuments(): pass

@Data(description="IR topics")
class AdhocTopics(): pass

@Data(description="IR assessments")
class AdhocAssessments(): pass

@Argument("documents", type=AdhocDocuments)
@Argument("topics", type=AdhocTopics)
@Argument("assessments", type=AdhocAssessments)
@DataTasks("information retrieval")
@Data()
class Adhoc(): pass