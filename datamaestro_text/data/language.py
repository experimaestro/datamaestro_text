from pathlib import Path
from datamaestro.data import Generic, Data, Argument
from datamaestro.data.ml import Supervised

@Argument("train", type=Generic)
@Argument("test", type=Generic, required=False)
@Argument("validation", type=Generic, required=False)
@Data("A dataset used for training language models")
class LanguageModelData(Supervised): pass