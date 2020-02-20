from datamaestro.data.ml import FolderBased, Supervised
from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.download.archive import tardownloader


@tardownloader("data", "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz")
@dataset(Supervised, url="http://ai.stanford.edu/~amaas/data/sentiment/", id="")
def aclimdb(data):
    """Large Movie Review Dataset

  Paper http://ai.stanford.edu/~amaas/papers/wvSent_acl2011.pdf
  """
    return {
        "train": FolderBased(path=data / "train", classes=["neg", "pos"]),
        "test": FolderBased(path=data / "test", classes=["neg", "pos"]),
    }
