from functools import cached_property
from pathlib import Path

from experimaestro import Param, Meta
from datamaestro.record import Record, RecordType
import datamaestro_text.data.ir as ir
from datamaestro_text.data.ir.base import IDItem, SimpleTextItem
from datamaestro_text.interfaces.plaintext import read_tsv


class AdhocRunWithText(ir.AdhocRun):
    "(qid, doc.id, query, passage)"

    path: Meta[Path]
    separator: Meta[str] = "\t"


class Topics(ir.Topics):
    "Pairs of query id - query using a separator"

    path: Meta[Path]
    separator: Meta[str] = "\t"

    def iter(self):
        return (
            Record(IDItem(qid), SimpleTextItem(title))
            for qid, title in read_tsv(self.path)
        )

    @cached_property
    def topic_recordtype(self) -> RecordType:
        """The class for topics"""
        return RecordType(IDItem, SimpleTextItem)


class Documents(ir.Documents):
    "One line per document, format pid<SEP>text"

    path: Param[Path]
    separator: Meta[str] = "\t"

    pass
