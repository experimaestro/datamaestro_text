from datamaestro.data.ml import FolderBased, Supervised
from datamaestro.definitions import  DataTasks, DataTags, Dataset
from datamaestro.download.archive import TarDownloader

@TarDownloader("data", "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz")
@Dataset(Supervised, url="http://ai.stanford.edu/~amaas/data/sentiment/", id="")
def aclimdb(data):
  """Large Movie Review Dataset

  Paper http://ai.stanford.edu/~amaas/papers/wvSent_acl2011.pdf
  """
  return {
    "train": FolderBased(path=data / "train", classes=["pos", "neg"]),
    "test": FolderBased(path=data / "test", classes=["pos", "neg"])
  }