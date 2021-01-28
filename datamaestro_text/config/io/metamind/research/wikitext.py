from datamaestro.data import Base, File
from datamaestro.definitions import (
    data,
    argument,
    datatasks,
    datatags,
    dataset,
    metadataset,
)
from datamaestro.download.archive import zipdownloader
from datamaestro_text.data.text import TrainingText


@datatags("text")
@datatasks("language modeling")
@metadataset(TrainingText)
def WikiText(data, type):
    """WikiText-2

    WikiText language modeling dataset is a collection of over 100 million
    tokens extracted from the set of verified Good and Featured articles on
    Wikipedia. The dataset is available under the Creative Commons
    Attribution-ShareAlike License.

    Compared to the preprocessed version of Penn Treebank (PTB), WikiText-2 is over
    2 times larger and WikiText-103 is over 110 times larger. The WikiText dataset
    also features a far larger vocabulary and retains the original case, punctuation
    and numbers - all of which are removed in PTB. As it is composed of full
    articles, the dataset is well suited for models that can take advantage of long
    term dependencies.

    https://blog.einstein.ai/the-wikitext-long-term-dependency-language-modeling-dataset/
    """
    return {
        "train": File(path=data / ("wiki.train.%s" % type)),
        "validation": File(path=data / ("wiki.valid.%s" % type)),
        "test": File(path=data / ("wiki.test.%s" % type)),
    }


@zipdownloader(
    "data", "https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-v1.zip"
)
@dataset(WikiText, id="2.tokens")
def wikitext_2_words(data):
    """The small wikitext corpus, already tokenized"""
    return WikiText(data, "tokens")


@zipdownloader(
    "data",
    "https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-raw-v1.zip",
)
@dataset(WikiText, id="2.raw")
def wikitext_2_raw(data):
    """The small wikitext corpus (raw data)"""
    return WikiText(data, "raw")


@zipdownloader(
    "data", "https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip"
)
@dataset(WikiText, id="103.tokens")
def wikitext_103_words(data):
    return WikiText(data, "tokens")


@zipdownloader(
    "data",
    "https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-raw-v1.zip",
)
@dataset(WikiText, id="103.raw")
def wikitext_103_raw(data):
    return WikiText(data, "raw")
