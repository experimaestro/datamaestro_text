"""
GloVe is an unsupervised learning algorithm for obtaining vector representations for words.
  Training is performed on aggregated global word-word co-occurrence statistics from a corpus,
  and the resulting representations showcase interesting linear substructures of the word vector space.
"""

from datamaestro.definitions import dataset
from datamaestro.download import reference
from datamaestro.download.archive import ZipDownloader
from datamaestro.download.single import FileDownloader
from datamaestro_text.data.embeddings import WordEmbeddingsText


# size: 822M
# statistics:
#   tokens: 6G
#   vocabulary: 400K
#   cased: false
@dataset(id="6b")
class Glove6B(WordEmbeddingsText):
    """Embeddings for 6B words in various dimensions"""

    EMBEDDINGS = ZipDownloader(
        "embeddings", "http://nlp.stanford.edu/data/glove.6B.zip"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.EMBEDDINGS.path)


@dataset(id="6b.50")
class Glove6B50(WordEmbeddingsText):
    """Glove 6B - dimension 50"""

    DATA_6B = reference(varname="data_6b", reference=Glove6B)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DATA_6B.prepare().path / "glove.6B.50d.txt")


@dataset(id="6b.100")
class Glove6B100(WordEmbeddingsText):
    """Glove 6B - dimension 100"""

    DATA_6B = reference(varname="data_6b", reference=Glove6B)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DATA_6B.prepare().path / "glove.6B.100d.txt")


@dataset(id="6b.200")
class Glove6B200(WordEmbeddingsText):
    """Glove 6B - dimension 200"""

    DATA_6B = reference(varname="data_6b", reference=Glove6B)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DATA_6B.prepare().path / "glove.6B.200d.txt")


...


@dataset(id="6b.300")
class Glove6B300(WordEmbeddingsText):
    """Glove 6B - dimension 200"""

    DATA_6B = reference(varname="data_6b", reference=Glove6B)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DATA_6B.prepare().path / "glove.6B.200d.txt")


@dataset(id="42b")
# size: 2.03G
# statistics:
#   cased: true
#   tokens: 42B
#   vocabulary: 2.2M
#   dimension: 300
class Glove42B(WordEmbeddingsText):
    """Glove embeddings trained on Common Crawl with 42B tokens"""

    EMBEDDINGS = FileDownloader(
        "embeddings", "http://nlp.stanford.edu/data/glove.42B.300d.zip"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.EMBEDDINGS.path)


@dataset(id="840b")
# size: 2.03G
# statistics:
#   cased: true
#   tokens: 840G
#   vocabulary: 2.2M
#   dimension: 300
class Glove840B(WordEmbeddingsText):
    """Glove embeddings trained on Common Crawl with 840B tokens"""

    EMBEDDINGS = FileDownloader(
        "embeddings", "http://nlp.stanford.edu/data/glove.840B.300d.zip"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.EMBEDDINGS.path)
