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
  return { "path": documents }

@LinkFolder("documents", "AP89", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/AP"])
@TIPSTER
def ap89(documents):
  """Associated Press document collection (1989)"""
  return { "path": documents }

@LinkFolder("documents", "AP90", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/AP"])
@TIPSTER
def ap90(documents):
  """Associated Press document collection (1990)"""
  return { "path": documents }


@LinkFolder("documents", "DOE1", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/DOE"])
@TIPSTER
def doe1(documents):
  """Department of Energy documents"""
  return { "path": documents }



# --- Wall Street Journal (1987-92)

@LinkFolder("documents", "1987", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/WSJ"])
@TIPSTER
def wsj87(documents):
  """Wall Street Journal (1987)"""
  return { "path": documents }

@LinkFolder("documents", "1988", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/WSJ"])
@TIPSTER
def wsj88(documents):
  """Wall Street Journal (1988)"""
  return { "path": documents }

@LinkFolder("documents", "1989", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/WSJ"])
@TIPSTER
def wsj89(documents):
  """Wall Street Journal (1989)"""
  return { "path": documents }

@LinkFolder("documents", "1990", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/WSJ"])
@TIPSTER
def wsj90(documents):
  """Wall Street Journal (1990)"""
  return { "path": documents }

@LinkFolder("documents", "1991", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/WSJ"])
@TIPSTER
def wsj91(documents):
  """Wall Street Journal (1991)"""
  return { "path": documents }

@LinkFolder("documents", "1992", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/WSJ"])
@TIPSTER
def wsj92(documents):
  """Wall Street Journal (1992)"""
  return { "path": documents }


# --- Federal Register (1988-89)


@LinkFolder("documents", "FR88", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/FR"])
@TIPSTER
def fr88(documents):
  """Federal Register (1988)"""
  return { "path": documents }

@LinkFolder("documents", "FR89", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/FR"])
@TIPSTER
def fr89(documents):
  """Federal Register (1989)"""
  return { "path": documents }

@LinkFolder("documents", "FR94", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/FR"])
@TIPSTER
def fr94(documents):
  """Federal Register (1994)"""
  return { "path": documents }


# # ZIFF (1988-92)


@LinkFolder("documents", "ZIFF1", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/ZIFF"])
@TIPSTER
def ziff1(documents):
  """Ziff/Davis document collection"""
  return { "path": documents }

@LinkFolder("documents", "ZIFF2", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/ZIFF"])
@TIPSTER
def ziff2(documents):
  """ Ziff/Davis document collection (1989-90)"""
  return { "path": documents }

@LinkFolder("documents", "ZIFF3", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/ZIFF"])
@TIPSTER
def ziff3(documents):
  """ Ziff/Davis document collection (1991-92)"""
  return { "path": documents }

# # SJM1


@LinkFolder("documents", "SJM1", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/SJM"])
@TIPSTER
def sjm1(documents):
  """San Jose Mercury News (1991)"""
  return { "path": documents }

# # CR1
@LinkFolder("documents", "CR1", ["%TIPSTER_DATADIR%", "%TIPSTER_DATADIR%/SJM"])
@TIPSTER
def cr1(documents):
  """TODO"""
  return { "path": documents }

# # FT1
@LinkFolder("documents", "FT1", ["%TIPSTER_DATADIR%"])
@TIPSTER
def ft1(documents):
  """Financial Times"""
  return { "path": documents }

# # FBIS1
@LinkFolder("documents", "FBIS", ["%TIPSTER_DATADIR%"])
@TIPSTER
def fbis1(documents):
  """TODO"""
  return { "path": documents }
# ---
# # FBIS1
@LinkFolder("documents", "LATIMES", ["%TIPSTER_DATADIR%"])
@TIPSTER
def la8990(documents):
  """Los Angeles Times (1989-90)"""
  return { "path": documents }
