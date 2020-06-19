"""Generic data types for information retrieval"""

from pathlib import Path
from datamaestro.definitions import data, argument, datatasks, datatags
from datamaestro.data import Base


@data(description="IR documents")
class AdhocDocuments(Base):
    pass


@data(description="IR topics")
class AdhocTopics(Base):
    pass

@data(description="IR assessments")
class AdhocAssessments(Base):
    pass


@data(description="IR adhoc run")
class AdhocRun(Base):
    pass


@argument("documents", type=AdhocDocuments)
@argument("topics", type=AdhocTopics)
@argument("assessments", type=AdhocAssessments)
@datatasks("information retrieval")
@data(description="An Adhoc IR collection")
class Adhoc(Base):
    pass

@argument("run", type=AdhocRun)
@data(description="Re-ranking task")
class RerankAdhoc(Adhoc):
    pass