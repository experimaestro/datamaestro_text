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


@data(description="IR adhoc results")
class AdhocResults(Base):
    pass


@argument("documents", type=AdhocDocuments)
@argument("topics", type=AdhocTopics)
@argument("assessments", type=AdhocAssessments)
@datatasks("information retrieval")
@data()
class Adhoc(Base):
    pass
