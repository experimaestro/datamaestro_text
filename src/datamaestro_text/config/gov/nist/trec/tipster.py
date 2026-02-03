"""

TIPSTER is sometimes also called the Text Research Collection Volume or TREC.

The TIPSTER project was sponsored by the Software and Intelligent Systems Technology
Office of the Advanced Research Projects Agency (ARPA/SISTO) in an effort to significantly
advance the state of the art in effective document detection (information retrieval) and
data extraction from large, real-world data collections.

The detection data is comprised of a test collection built at NIST for the TIPSTER project
and the related TREC project. The TREC project has many other participating information
retrieval research groups, working on the same task as the TIPSTER groups, but meeting
once a year in a workshop to compare results (similar to MUC). The test collection consists
of three CD-ROMs of SGML encoded documents distributed by LDC plus queries and answers
(relevant documents) distributed by NIST.

See also https://trec.nist.gov/data/docs_eng.html and https://trec.nist.gov/data/intro_eng.html
"""

from datamaestro_text.data.ir.trec import TipsterCollection
from datamaestro.download.links import linkfolder
from datamaestro.definitions import (
    Dataset,
    dataset,
)
from datamaestro.context import DatafolderPath

# Store meta-information
TIPSTER = dataset(url="https://catalog.ldc.upenn.edu/LDC93T3A")


@TIPSTER
class Ap88(Dataset):
    """Associated Press document collection (1988)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/AP")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Ap89(Dataset):
    """Associated Press document collection (1989)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/AP")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Ap90(Dataset):
    """Associated Press document collection (1990)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk3/AP")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Doe1(Dataset):
    """Department of Energy documents"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/DOE")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


# --- Wall Street Journal (1987-92)


@TIPSTER
class Wsj87(Dataset):
    """Wall Street Journal (1987)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/WSJ/1987")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Wsj88(Dataset):
    """Wall Street Journal (1988)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/WSJ/1988")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Wsj89(Dataset):
    """Wall Street Journal (1989)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/WSJ/1989")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Wsj90(Dataset):
    """Wall Street Journal (1990)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/WSJ/1990")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Wsj91(Dataset):
    """Wall Street Journal (1991)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/WSJ/1991")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Wsj92(Dataset):
    """Wall Street Journal (1992)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/WSJ/1992")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


# --- Federal Register (1988-89)


@TIPSTER
class Fr88(Dataset):
    """Federal Register (1988)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/FR")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Fr89(Dataset):
    """Federal Register (1989)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/FR")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Fr94(Dataset):
    """Federal Register (1994)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk4/FR94")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


# # ZIFF (1988-92)


@TIPSTER
class Ziff1(Dataset):
    """Information from the Computer Select disks (1989-90)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/ZIFF")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Ziff2(Dataset):
    """Information from the Computer Select disks (1989-90)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/ZIFF")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Ziff3(Dataset):
    """Information from the Computer Select disks (1990-91)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk3/ZIFF")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Sjm1(Dataset):
    """San Jose Mercury News (1991)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk3/SJM")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Cr1(Dataset):
    """TODO"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk4/CR")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Ft1(Dataset):
    """Financial Times"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk4/FT")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class Fbis1(Dataset):
    """Foreign Broadcast Information Service (1996)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk5/FBIS")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)


@TIPSTER
class La8990(Dataset):
    """Los Angeles Times (1989-90)"""

    DOCUMENTS = linkfolder(
        "documents", [DatafolderPath("gov.nist.trec.tipster", "Disk5/LATIMES")]
    )

    def config(self) -> TipsterCollection:
        return TipsterCollection.C(path=self.DOCUMENTS.path)
