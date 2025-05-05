from typing import Optional
from experimaestro import Param
from datamaestro.data import Base, Folder, File
from datamaestro.data.ml import Supervised


class TrainingText(Supervised):
    """ "A dataset used for training with a train and a test"""

    train: Param[Base]
    test: Param[Optional[Base]] = None
    validation: Param[Optional[Base]] = None


class TextFolder(Folder):
    "A folder composed of texts"
    pass


class TextFile(File):
    """A file composed of texts"""

    pass
