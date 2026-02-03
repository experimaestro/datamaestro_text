from datamaestro.definitions import Dataset, dataset
from datamaestro.download.single import FileDownloader
from datamaestro_text.data.text import TextFile
from datamaestro.utils import HashCheck


@dataset(url="https://oscar-corpus.com/", size="2.3T")
class English(Dataset):
    """Huge French corpus from INRIA

    OSCAR or Open Super-large Crawled ALMAnaCH coRpus is a huge multilingual corpus
    obtained by language classification and filtering of the Common Crawl corpus using
    the goclassy architecture.
    """

    FILE = FileDownloader(
        "file",
        "https://oscar-public.huma-num.fr/shuffled/en_dedup.txt.gz",
        checker=HashCheck("5c906ede3c5265f8934b62c275a754bc"),
    )

    def config(self) -> TextFile:
        return TextFile.C(path=self.FILE.path)
