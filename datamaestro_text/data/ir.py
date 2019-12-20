from pathlib import Path
from datamaestro.definitions import data, argument, datatasks, datatags

@data(description="IR documents")
class AdhocDocuments(): pass

@data(description="IR topics")
class AdhocTopics(): pass

@data(description="IR assessments")
class AdhocAssessments(): pass

@argument("documents", type=AdhocDocuments)
@argument("topics", type=AdhocTopics)
@argument("assessments", type=AdhocAssessments)
@datatasks("information retrieval")
@data()
class Adhoc(): pass