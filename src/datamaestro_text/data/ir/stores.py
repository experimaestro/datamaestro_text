from collections import namedtuple
from typing import List, NamedTuple
from experimaestro import Constant
import attrs

from datamaestro.record import Record
from datamaestro_text.data.ir.base import IDItem
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
