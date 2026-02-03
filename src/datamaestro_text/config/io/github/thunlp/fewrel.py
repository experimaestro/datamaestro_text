# See documentation on https://datamaestro.readthedocs.io

from datamaestro.data import File
from datamaestro.data.ml import Supervised
from datamaestro.definitions import Dataset, datatasks, datatags, dataset
from datamaestro.download.single import FileDownloader
from datamaestro.utils import HashCheck


@datatags("unsupervised")
@datatasks("information extraction")
@dataset(
    url="https://thunlp.github.io/1/fewrel1.html",
)
class V1(Dataset):
    """FewRel 1.0 - a Few-shot Relation classification dataset

    FewRel is a Few-shot Relation classification dataset, which features 70, 000 natural
    language sentences expressing 100 relations annotated by crowdworkers.

    Only the train and validation dataset are available. The test set is hidden
    for the leaderboard.
    """

    TRAIN = FileDownloader(
        "train.json",
        "https://github.com/thunlp/FewRel/raw/master/data/train_wiki.json",
        checker=HashCheck("5e663e9c3f1bfbdb2de72696e9504fd7"),
    )
    VALIDATION = FileDownloader(
        "validation.json",
        "https://github.com/thunlp/FewRel/raw/master/data/val_wiki.json",
        checker=HashCheck("3f25573428c0332cb64b367a275ab0c7"),
    )

    def config(self) -> Supervised:
        return Supervised.C(
            train=File.C(path=self.TRAIN.path),
            validation=File.C(path=self.VALIDATION.path),
        )
