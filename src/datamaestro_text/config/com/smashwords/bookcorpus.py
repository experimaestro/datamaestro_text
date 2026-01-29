# See documentation on https://datamaestro.readthedocs.io

from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro_text.data.text import TextFolder
from datamaestro.download.archive import TarDownloader
from datamaestro.utils import HashCheck


@datatags("text", "books", "English")
@datatasks("language modeling")
@dataset(id="", url="https://yknzhu.wixsite.com/mbweb", size="4.3G")
class Main(TextFolder):
    """Unpublished books from Smashwords

    The books are concatened in two files hosted on huggingface NLP storage.
    Each sentence is on a separate line and tokens are space separated.
    """

    FOLDER = TarDownloader(
        "folder",
        "https://storage.googleapis.com/huggingface-nlp/datasets/bookcorpus/bookcorpus.tar.bz2",
        checker=HashCheck("5c906ede3c5265f8934b62c275a754bc"),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FOLDER.path)
