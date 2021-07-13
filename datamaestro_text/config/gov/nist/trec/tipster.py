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

from datamaestro.data import Base
from datamaestro_text.data.ir.trec import TipsterCollection
from datamaestro.download.links import linkfolder
from datamaestro.definitions import (
    dataset,
    DatafolderPath,
)

TIPSTER = dataset(TipsterCollection, url="https://catalog.ldc.upenn.edu/LDC93T3A")


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/AP")])
@TIPSTER
def ap88(documents):
    """Associated Press document collection (1988)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/AP")])
@TIPSTER
def ap89(documents):
    """Associated Press document collection (1989)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk3/AP")])
@TIPSTER
def ap90(documents):
    """Associated Press document collection (1990)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/DOE")])
@TIPSTER
def doe1(documents):
    """Department of Energy documents"""
    return {"path": documents}


# --- Wall Street Journal (1987-92)


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/WSJ/1987")])
@TIPSTER
def wsj87(documents):
    """Wall Street Journal (1987)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/WSJ/1988")])
@TIPSTER
def wsj88(documents):
    """Wall Street Journal (1988)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/WSJ/1989")])
@TIPSTER
def wsj89(documents):
    """Wall Street Journal (1989)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/WSJ/1990")])
@TIPSTER
def wsj90(documents):
    """Wall Street Journal (1990)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/WSJ/1991")])
@TIPSTER
def wsj91(documents):
    """Wall Street Journal (1991)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/WSJ/1992")])
@TIPSTER
def wsj92(documents):
    """Wall Street Journal (1992)"""
    return {"path": documents}


# --- Federal Register (1988-89)


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/FR")])
@TIPSTER
def fr88(documents):
    """Federal Register (1988)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/FR")])
@TIPSTER
def fr89(documents):
    """Federal Register (1989)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk4/FR94")])
@TIPSTER
def fr94(documents):
    """Federal Register (1994)"""
    return {"path": documents}


# # ZIFF (1988-92)


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk1/ZIFF")])
@TIPSTER
def ziff1(documents):
    """Information from the Computer Select disks (1989-90)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk2/ZIFF")])
@TIPSTER
def ziff2(documents):
    """Information from the Computer Select disks (1989-90)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk3/ZIFF")])
@TIPSTER
def ziff3(documents):
    """Information from the Computer Select disks (1990-91)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk3/SJM")])
@TIPSTER
def sjm1(documents):
    """San Jose Mercury News (1991)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk4/CR")])
@TIPSTER
def cr1(documents):
    """TODO"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk4/FT")])
@TIPSTER
def ft1(documents):
    """Financial Times"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk5/FBIS")])
@TIPSTER
def fbis1(documents):
    """Foreign Broadcast Information Service (1996)"""
    return {"path": documents}


@linkfolder("documents", [DatafolderPath("gov.nist.trec.tipster", "Disk5/LATIMES")])
@TIPSTER
def la8990(documents):
    """Los Angeles Times (1989-90)"""
    return {"path": documents}
