import json
from pathlib import Path
from typing import List, NamedTuple
from experimaestro import Constant, Meta

from datamaestro.record import Record
from datamaestro_text.data.ir.base import (
    DocumentRecord,
    IDItem,
    SimpleTextItem,
    TextItem,
    UrlItem,
)
from datamaestro_text.datasets.irds.data import LZ4DocumentStore
from datamaestro_text.data.ir.formats import OrConvQADocument


class OrConvQADocumentStore(LZ4DocumentStore):
    class NAMED_TUPLE(NamedTuple):
        id: str
        title: str
        body: str
        aid: str
        bid: int

    lookup_field: Constant[str] = "id"
    fields: Constant[List[str]] = list(NAMED_TUPLE._fields)
    index_fields: Constant[List[str]] = ["id"]

    data_cls = NAMED_TUPLE

    def converter(self, data: NAMED_TUPLE) -> Record:
        fields = data._asdict()
        del fields["id"]
        return Record(OrConvQADocument(**fields), IDItem(data.id))


def jsonl_reader(path: Path, suffix: str, *, opener: open):
    for path in path.glob(f"*{suffix}"):
        with opener(path, "rt") as fp:
            for ix, line in enumerate(fp):
                yield json.loads(line)


class IKatClueWeb22DocumentStore(LZ4DocumentStore):
    @staticmethod
    def generator(path: Path, suffix: str, *, opener: open):
        def __iter__():
            iterator = jsonl_reader(path, suffix, opener=opener)
            yield from map(
                lambda data, *_: IKatClueWeb22DocumentStore.Document(**data), iterator
            )

        return __iter__

    class Document(NamedTuple):
        id: str
        contents: str
        url: str

    data_cls = Document
    lookup_field: Constant[str] = "id"
    index_fields: Constant[List[str]] = ["id"]

    def converter(self, data):
        return DocumentRecord(
            IDItem(data.id), SimpleTextItem(data.contents), UrlItem(data.url)
        )
