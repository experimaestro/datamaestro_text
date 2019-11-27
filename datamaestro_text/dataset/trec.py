from datamaestro.dataset import Dataset
from datamaestro.experimaestro import Argument, Type
from pathlib import Path

@Argument("files", type=Path)
@Type("text.documents", description="A collection of (text) documents")
class DocumentCollection(Dataset): pass

@Argument("files", type=Path)
@Type("gov.nist.trec.tipster", description="TREC collection")
class TipsterCollection(DocumentCollection): pass