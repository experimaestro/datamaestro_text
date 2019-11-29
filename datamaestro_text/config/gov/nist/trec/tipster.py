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
"""

from datamaestro.data import Generic
from datamaestro_text.data.trec import TipsterCollection
from datamaestro.download.manual import LinkFolder
from datamaestro.definitions import Data, Argument, Type, DataTasks, DataTags, Dataset

TIPSTER = Dataset(TipsterCollection, url="https://catalog.ldc.upenn.edu/LDC93T3A")

@LinkFolder("documents", "AP88", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/AP"])
@TIPSTER
def ap88(documents):
  """Associated Press document collection (1988)"""
  return { "path": documents.path }

@LinkFolder("documents", "AP89", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/AP"])
@TIPSTER
def ap89(documents):
  """Associated Press document collection (1989)"""
  return { "path": documents.path }

@LinkFolder("documents", "AP90", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/AP"])
@TIPSTER
def ap90(documents):
  """Associated Press document collection (1990)"""
  return { "path": documents.path }


@LinkFolder("documents", "DOE1", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/DOE"])
@TIPSTER
def doe1(documents):
  """Department of Energy documents"""
  return { "path": documents.path }



# # Wall Street Journal
# ---
# id: wsj87
# description: Wall Street Journal (1987)
# download: !@/manual:DownloadPath 
#   name: "1987"
#   search: [ "%TIPSTER_DATADIR%/WSJ"]
# ...
# ---
# id: wsj88
# description: Wall Street Journal (1988)
# download: !@/manual:DownloadPath 
#   name: "1988"
#   search: [ "%TIPSTER_DATADIR%/WSJ"]
# ...
# ---
# id: wsj89
# description: Wall Street Journal (1989)
# download: !@/manual:DownloadPath 
#   name: "1989"
#   search: [ "%TIPSTER_DATADIR%/WSJ"]
# ...
# ---
# id: wsj90
# description: Wall Street Journal (1990)
# download: !@/manual:DownloadPath 
#   name: "1990"
#   search: [ "%TIPSTER_DATADIR%/WSJ"]
# ...
# ---
# id: wsj91
# description: Wall Street Journal (1991)
# download: !@/manual:DownloadPath 
#   name: "1991"
#   search: [ "%TIPSTER_DATADIR%/WSJ"]
# ...
# ---
# id: wsj92
# description: Wall Street Journal (1992)
# download: !@/manual:DownloadPath 
#   name: "1992"
#   search: [ "%TIPSTER_DATADIR%/WSJ"]
# ...


# # Federal Register (1988-89)

# ---
# id: fr88
# description: Federal Register (1988)
# download: !@/manual:DownloadPath 
#   name: FR88
#   search: ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/FR"]
# ...
# ---
# id: fr89
# description: Federal Register (1989)
# download: !@/manual:DownloadPath 
#   name: FR89
#   search: ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/FR"]
# ...
# ---
# id: fr94
# description: Federal Register (1994)
# download: !@/manual:DownloadPath 
#   name: FR94
#   search: ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/FR"]
# ...


# # ZIFF (1988-92)

# ---
# id: ziff1
# description: Ziff/Davis document collection
# download: !@/manual:DownloadPath 
#   name: ZIFF1
#   search: ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/ZIFF"]
# ...
# ---
# id: ziff2
# description:  Ziff/Davis document collection (1989-90)
# download: !@/manual:DownloadPath 
#   name: ZIFF2
#   search: ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/ZIFF"]
# ...
# ---
# id: ziff3
# description:  Ziff/Davis document collection (1991-92)
# download: !@/manual:DownloadPath 
#   name: ZIFF3
#   search: ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/ZIFF"]
# ...

# # SJM1

# ---
# id: sjm1
# description: San Jose Mercury News (1991)
# download: !@/manual:DownloadPath 
#   name: SJM1
#   search: ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/SJM"]
# ...
# ---
# # CR1
# id: cr1
# description: TODO
# download: !@/manual:DownloadPath 
#   name: CR1
#   search: ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/SJM"]
# ...
# ---
# # FT1
# id: ft1
# description: Financial Times
# download: !@/manual:DownloadPath 
#   name: FT1
#   search: ["%TIPSTER_DATADIR%"]
# ...
# ---
# # FBIS1
# id: fbis1
# description: TODO
# download: !@/manual:DownloadPath 
#   name: FBIS
#   search: ["%TIPSTER_DATADIR%"]
# ...
# ---
# # FBIS1
# id: la8990
# description: Los Angeles Times (1989-90)
# download: !@/manual:DownloadPath 
#   name: LATIMES
#   search: ["%TIPSTER_DATADIR%"]

