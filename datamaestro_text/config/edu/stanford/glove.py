"""
GloVe is an unsupervised learning algorithm for obtaining vector representations for words.
  Training is performed on aggregated global word-word co-occurrence statistics from a corpus,
  and the resulting representations showcase interesting linear substructures of the word vector space.
"""

from datamaestro.definitions import dataset
from datamaestro.data import Base, Generic
from datamaestro.download import reference
from datamaestro.download.archive import zipdownloader
from datamaestro.download.single import filedownloader
from datamaestro_text.data.embeddings import WordEmbeddingsText

# size: 822M
# statistics:
#   tokens: 6G
#   vocabulary: 400K
#   cased: false
@zipdownloader("embeddings", "http://nlp.stanford.edu/data/glove.6B.zip")
@dataset(WordEmbeddingsText, id="6b")
def glove_6b(embeddings):
    """Embeddings for 6B words in various dimensions"""
    return {"path": embeddings}


@reference("data_6b", glove_6b)
@dataset(WordEmbeddingsText, id="6b.50")
def glove_6b_50(data_6b):
    """Glove 6B - dimension 50"""
    return {"path": data_6b.path / "glove.6B.50d.txt"}


@reference("data_6b", glove_6b)
@dataset(WordEmbeddingsText, id="6b.100")
def glove_6b_100(data_6b):
    """Glove 6B - dimension 100"""
    return {"path": data_6b.path / "glove.6B.100d.txt"}


@reference("data_6b", glove_6b)
@dataset(WordEmbeddingsText, id="6b.200")
def glove_6b_200(data_6b):
    """Glove 6B - dimension 200"""
    return {"path": data_6b.path / "glove.6B.200d.txt"}


...


@reference("data_6b", glove_6b)
@dataset(WordEmbeddingsText, id="6b.300")
def glove_6b_300(data_6b):
    """Glove 6B - dimension 200"""
    return {"path": data_6b.path / "glove.6B.200d.txt"}


@filedownloader("embeddings", "http://nlp.stanford.edu/data/glove.42B.300d.zip")
@dataset(WordEmbeddingsText, id="42b")
# size: 2.03G
# statistics:
#   cased: true
#   tokens: 42B
#   vocabulary: 2.2M
#   dimension: 300
def glove_42b(embeddings):
    """Glove embeddings trained on Common Crawl with 42B tokens"""
    return {"path": embeddings}


@filedownloader("embeddings", "http://nlp.stanford.edu/data/glove.840B.300d.zip")
@dataset(WordEmbeddingsText, id="840b")
# size: 2.03G
# statistics:
#   cased: true
#   tokens: 840G
#   vocabulary: 2.2M
#   dimension: 300
def glove_840b(embeddings):
    """Glove embeddings trained on Common Crawl with 840B tokens"""
    return {"path": embeddings}
