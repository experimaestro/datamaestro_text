"""The AQUAINT Corpus, Linguistic Data Consortium (LDC) catalog number LDC2002T31 and ISBN 1-58563-240-6 consists of newswire text data in English, drawn from three sources: the Xinhua News Service (People's Republic of China), the New York Times News Service, and the Associated Press Worldstream News Service. It was prepared by the LDC for the AQUAINT Project, and will be used in official benchmark evaluations conducted by National Institute of Standards and Technology (NIST)."""

from datamaestro.context import DatafolderPath
from datamaestro.definitions import Dataset, dataset
from datamaestro.download.links import links, linkfolder
from datamaestro_text.data.ir.trec import TipsterCollection


URL = "https://catalog.ldc.upenn.edu/LDC2002T31"


@dataset(url=URL, id=".apw")
class Apw(Dataset):
    """Associated Press (1998-2000)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("edu.upenn.ldc.aquaint", "APW")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@dataset(url=URL, id=".nyt")
class Nyt(Dataset):
    """New York Times (1998-2000)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("edu.upenn.ldc.aquaint", "NYT")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@dataset(url=URL, id=".xie")
class Xie(Dataset):
    """Xinhua News Agency newswires (1996-2000)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("edu.upenn.ldc.aquaint", "XIE")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@dataset(url=URL, id="")
class Aquaint(Dataset):
    """Aquaint documents"""

    DOCUMENTS = links("documents", apw=Apw, nyt=Nyt, xie=Xie)

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)
