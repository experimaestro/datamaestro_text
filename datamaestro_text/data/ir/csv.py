from pathlib import Path

from datamaestro.definitions import argument, data, datatags, datatasks
import datamaestro_text.data.ir as ir

@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@data(description="(qid, doc.id, query, passage)")
class AdhocRunWithText(ir.AdhocRun): 
    pass

@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@data(description="Pairs of query id - query using a separator")
class AdhocTopics(ir.AdhocTopics): 
    pass


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
@data(description="One line per document, format pid<SEP>text")
class AdhocDocuments(ir.AdhocDocuments): 
    pass
