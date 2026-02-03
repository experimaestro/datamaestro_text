from datamaestro.data.ml import FolderBased, Supervised
from datamaestro.definitions import Dataset, dataset
from datamaestro.download.archive import TarDownloader


@dataset(url="http://ai.stanford.edu/~amaas/data/sentiment/", id="")
class Aclimdb(Dataset):
    """Large Movie Review Dataset

    Paper http://ai.stanford.edu/~amaas/papers/wvSent_acl2011.pdf
    """

    DATA = TarDownloader(
        "data", "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
    )

    def config(self) -> Supervised:
        return Supervised.C(
            train=FolderBased.C(path=self.DATA.path / "train", classes=["neg", "pos"]),
            test=FolderBased.C(path=self.DATA.path / "test", classes=["neg", "pos"]),
        )
