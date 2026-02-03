from datamaestro.data import File
from datamaestro.definitions import (
    Dataset,
    datatasks,
    datatags,
    dataset,
    metadataset,
)
from datamaestro.download.archive import ZipDownloader
from datamaestro_text.data.text import TrainingText


def _wikitext(data, type):
    """Helper to build a TrainingText from data path and type."""
    return TrainingText.C(
        train=File.C(path=data / ("wiki.train.%s" % type)),
        validation=File.C(path=data / ("wiki.valid.%s" % type)),
        test=File.C(path=data / ("wiki.test.%s" % type)),
    )


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
    return _wikitext(data, type)


@dataset(WikiText, id=".2.tokens")
class Wikitext2Words(Dataset):
    """The small wikitext corpus, already tokenized"""

    DATA = ZipDownloader(
        "data",
        "https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-v1.zip",
    )

    def config(self) -> TrainingText:
        return _wikitext(self.DATA.path, "tokens")


@dataset(WikiText, id=".2.raw")
class Wikitext2Raw(Dataset):
    """The small wikitext corpus (raw data)"""

    DATA = ZipDownloader(
        "data",
        "https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-raw-v1.zip",
    )

    def config(self) -> TrainingText:
        return _wikitext(self.DATA.path, "raw")


@dataset(WikiText, id=".103.tokens")
class Wikitext103Words(Dataset):
    DATA = ZipDownloader(
        "data",
        "https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip",
    )

    def config(self) -> TrainingText:
        return _wikitext(self.DATA.path, "tokens")


@dataset(WikiText, id=".103.raw")
class Wikitext103Raw(Dataset):
    DATA = ZipDownloader(
        "data",
        "https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-raw-v1.zip",
    )

    def config(self) -> TrainingText:
        return _wikitext(self.DATA.path, "raw")
