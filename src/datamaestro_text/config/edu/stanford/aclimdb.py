from datamaestro.data.ml import FolderBased, Supervised
from datamaestro.definitions import dataset
from datamaestro.download.archive import TarDownloader


@dataset(url="http://ai.stanford.edu/~amaas/data/sentiment/", id="")
class Aclimdb(Supervised):
    """Large Movie Review Dataset

    Paper http://ai.stanford.edu/~amaas/papers/wvSent_acl2011.pdf
    """

    DATA = TarDownloader(
        "data", "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            train=FolderBased.C(path=cls.DATA.path / "train", classes=["neg", "pos"]),
            test=FolderBased.C(path=cls.DATA.path / "test", classes=["neg", "pos"]),
        )
