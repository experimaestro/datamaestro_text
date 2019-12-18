from pathlib import Path
from datamaestro.experimaestro import Any
from datamaestro.data import Generic, data, argument
from datamaestro.data.ml import Supervised

@argument("train", type=Any)
@argument("test", type=Any, required=False)
@argument("validation", type=Any, required=False)
@data("A dataset used for training language models")
class LanguageModelData(Supervised): pass