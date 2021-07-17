from pathlib import Path
from datamaestro.data import Base, Folder, File, argument
from datamaestro.data.ml import Supervised


@argument("train", type=Base)
@argument("test", type=Base, required=False)
@argument("validation", type=Base, required=False)
class TrainingText(Supervised):
    """"A dataset used for training with a train and a test"""

    pass


class TextFolder(Folder):
    "A folder composed of texts"
    pass


class TextFile(File):
    """A file composed of texts"""

    pass
