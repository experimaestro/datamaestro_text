from pathlib import Path
from typing import Iterator, Tuple

from experimaestro import Param, Option, Constant
from datamaestro.definitions import argument, data, constant, datatags, datatasks
import datamaestro_text.data.ir as ir
from datamaestro_text.interfaces.plaintext import read_tsv


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
        return (
            ir.AdhocTopic(qid, title, None, None) for qid, title in read_tsv(self.path)
        )


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@data(description="One line per document, format pid<SEP>text")
class AdhocDocuments(ir.AdhocDocuments):
    pass


@data(description="Training triplets (query/document IDs only)")
class TrainingTripletsID(ir.TrainingTripletsLines):
    separator: Option[str] = "\t"
    documents: Param[ir.AdhocDocuments]
    topics: Param[ir.AdhocTopics]
    ids: Constant[bool] = True

    def iter(self) -> Iterator[Tuple[str, str, str]]:
        queries = {}
        for query in self.topics.iter():
            queries[query.qid] = query.title

        for qid, pos, neg in read_tsv(self.path):
            yield queries[qid], pos, neg


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@constant("ids", False)
@data(description="Training triplets (full text)")
class TrainingTriplets(ir.TrainingTriplets):
    def iter(self) -> Iterator[Tuple[str, str, str]]:
        yield from read_tsv(self.path)
