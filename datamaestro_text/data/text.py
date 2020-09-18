from pathlib import Path
from datamaestro.data import Base, Folder, File, data, argument
from datamaestro.data.ml import Supervised


@argument("train", type=Base)
@argument("test", type=Base, required=False)
@argument("validation", type=Base, required=False)
@data("A dataset used for training with a train and a test")
class TrainingText(Supervised):
    pass


@data("A folder composed of texts")
class TextFolder(Folder):
    pass


@data("A file composed of texts")
class TextFile(File):
    pass
