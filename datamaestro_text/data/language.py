from pathlib import Path
from datamaestro.data import Base, data, argument
from datamaestro.data.ml import Supervised


@argument("train", type=Base)
@argument("test", type=Base, required=False)
@argument("validation", type=Base, required=False)
@data("A dataset used for training language models")
class LanguageModelData(Supervised):
    pass
