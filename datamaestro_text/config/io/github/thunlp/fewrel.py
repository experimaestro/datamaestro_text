# See documentation on http://experimaestro.github.io/datamaestro/

from datamaestro.data import File
from datamaestro.data.ml import Supervised
from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.download.single import filedownloader
from datamaestro.utils import HashCheck


@datatags("unsupervised")
@datatasks("information extraction")
@filedownloader(
    "train.json",
    "https://github.com/thunlp/FewRel/raw/master/data/train_wiki.json",
    checker=HashCheck("5e663e9c3f1bfbdb2de72696e9504fd7"),
)
@filedownloader(
    "validation.json",
    "https://github.com/thunlp/FewRel/raw/master/data/val_wiki.json",
    checker=HashCheck("3f25573428c0332cb64b367a275ab0c7"),
)
@dataset(
    Supervised, url="https://thunlp.github.io/1/fewrel1.html",
)
def v1(train, validation):
    """FewRel 1.0 - a Few-shot Relation classification dataset

   FewRel is a Few-shot Relation classification dataset, which features 70, 000 natural
   language sentences expressing 100 relations annotated by crowdworkers.

   Only the train and validation dataset are available. The test set is hidden
   for the leaderboard.
  """
    return {"train": File(path=train), "validation": File(path=validation)}
