from pathlib import Path

from datamaestro.definitions import argument, data, datatags, datatasks
import datamaestro_text.data.ir as ir
from datamaestro_text.interfaces.plaintext import read_tsv
from datamaestro_text.interfaces.trec import Topic


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@data(description="(qid, doc.id, query, passage)")
class AdhocRunWithText(ir.AdhocRun):
    pass


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@data(description="Pairs of query id - query using a separator")
class AdhocTopics(ir.AdhocTopics):
    def iter(self):
        return (Topic(qid, title, None, None) for qid, title in read_tsv(self.path))


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@data(description="One line per document, format pid<SEP>text")
class AdhocDocuments(ir.AdhocDocuments):
    pass


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@argument("documents", type=ir.AdhocDocuments)
@argument("topics", ir.AdhocTopics)
@data(description="Training triplets (query/document IDs only)")
class TrainingTripletsID(ir.TrainingTriplets):
    pass


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@data(description="Training triplets (full text)")
class TrainingTriplets(ir.TrainingTriplets):
    pass
