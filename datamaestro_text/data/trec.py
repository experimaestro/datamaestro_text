from datamaestro.definitions import Argument, Data
from datamaestro.data import Generic
from pathlib import Path
from .ir import AdhocDocuments

@Argument("path", type=Path)
@Data()
class TipsterCollection(AdhocDocuments): pass
