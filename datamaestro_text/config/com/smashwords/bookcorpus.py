# See documentation on http://experimaestro.github.io/datamaestro/

from datamaestro.definitions import data, argument, datatasks, datatags, dataset
from datamaestro_text.data.text import TextFolder
from datamaestro.download.archive import tardownloader
from datamaestro.utils import HashCheck


@datatags("text", "books", "English")
@datatasks("language modeling")
@tardownloader(
    "folder",
    "https://storage.googleapis.com/huggingface-nlp/datasets/bookcorpus/bookcorpus.tar.bz2",
    checker=HashCheck("5c906ede3c5265f8934b62c275a754bc"),
)
@dataset(TextFolder, id="", url="https://yknzhu.wixsite.com/mbweb", size="4.3G")
def main(folder):
    """Unpublished books from Smashwords

    The books are concatened in two files hosted on huggingface NLP storage.
    Each sentence is on a separate line and tokens are space separated.
    """
    return {"path": folder}
