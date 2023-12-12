from collections import namedtuple
from typing import List
from experimaestro import Constant
import attrs

from datamaestro_text.datasets.irds.data import LZ4DocumentStore
from datamaestro_text.data.ir.formats import OrConvQADocument


class OrConvQADocumentStore(LZ4DocumentStore):
    NAMED_TUPLE = namedtuple(
        "OrConvQADocument", [a.name for a in attrs.fields(OrConvQADocument)]
    )

    lookup_field: Constant[str] = "id"
    fields: Constant[List[str]] = list(NAMED_TUPLE._fields)
    index_fields: Constant[List[str]] = ["id"]

    data_cls = NAMED_TUPLE

    def converter(self, data: NAMED_TUPLE) -> OrConvQADocument:
        return OrConvQADocument(**data._asdict())
