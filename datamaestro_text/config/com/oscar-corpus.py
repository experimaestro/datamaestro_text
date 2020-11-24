from datamaestro.definitions import data, argument, datatasks, datatags, dataset
from datamaestro.download.single import filedownloader
from datamaestro_text.data.text import TextFile
from datamaestro.utils import HashCheck


@filedownloader(
    "file",
    "https://oscar-public.huma-num.fr/shuffled/en_dedup.txt.gz",
    checker=HashCheck("5c906ede3c5265f8934b62c275a754bc"),
)
@dataset(TextFile, url="https://oscar-corpus.com/", size="2.3T")
def english(file):
    """Huge French corpus from INRIA

  OSCAR or Open Super-large Crawled ALMAnaCH coRpus is a huge multilingual corpus
  obtained by language classification and filtering of the Common Crawl corpus using
  the goclassy architecture.
  """
    return {"path": file}
