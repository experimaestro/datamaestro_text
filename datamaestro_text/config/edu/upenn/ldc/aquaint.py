"""The AQUAINT Corpus, Linguistic Data Consortium (LDC) catalog number LDC2002T31 and ISBN 1-58563-240-6 consists of newswire text data in English, drawn from three sources: the Xinhua News Service (People's Republic of China), the New York Times News Service, and the Associated Press Worldstream News Service. It was prepared by the LDC for the AQUAINT Project, and will be used in official benchmark evaluations conducted by National Institute of Standards and Technology (NIST)."""

from datamaestro.data import Generic
from datamaestro_text.data.trec import TipsterCollection
from datamaestro.download.manual import LinkFolder
from datamaestro.definitions import Data, Argument, Type, DataTasks, DataTags, Dataset
from datamaestro.download.links import Links


URL="https://catalog.ldc.upenn.edu/LDC2002T31"

@LinkFolder("documents", "APW", ["%AQUAINT_DATADIR%"])
@Dataset(TipsterCollection, url=URL, id="apw")
def apw(documents):
  """Associated Press (1998-2000)"""
  return { "path": documents }

@LinkFolder("documents", "NYT", ["%AQUAINT_DATADIR%"])
@Dataset(TipsterCollection, url=URL,id="nyt")
def nyt(documents):
  """New York Times (1998-2000)"""
  return { "path": documents }


@LinkFolder("documents", "XIE", ["%AQUAINT_DATADIR%"])
@Dataset(TipsterCollection, url=URL, id="xie")
def xie(documents):
  """Xinhua News Agency newswires (1996-2000)"""
  return { "path": documents }


@Links("documents", apw=apw.path, nyt=nyt.path, xie=xie.path)
@Dataset(TipsterCollection, url=URL, id="")
def aquaint(documents):
  """Aquaint dataset"""
  return { "path": documents }
