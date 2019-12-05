"""TREC AD-HOC datasets and tasks
"""

from datamaestro.data import Generic
from datamaestro.download import Reference
from datamaestro.download.single import FileDownloader, ConcatDownload
from datamaestro.download.links import Links
from datamaestro.stream import TransformList
from datamaestro.stream.compress import Gunzip
from datamaestro.stream.lines import Replace, Filter
from datamaestro.definitions import Data, Argument, Type, DataTasks, DataTags, Dataset

from datamaestro_text.data.trec import TipsterCollection, TrecTopics, TrecAssessments
from datamaestro_text.data.ir import Adhoc

from .tipster import *
from datamaestro_text.config.edu.upenn.ldc.aquaint import aquaint


# --- TREC 1 (1992)

@Links("documents",
  ap88=ap88.path, ap89=ap89.path, fr88=fr88.path, fr89=fr89.path,
  wsj87=wsj87.path, wsj88=wsj88.path, wsj89=wsj89.path,
  wsj90=wsj90.path, wsj91=wsj91.path, wsj92=wsj92.path,
  ziff1=ziff1.path, ziff2=ziff2.path)
@Dataset(TipsterCollection, id="1.documents")
def trec1_documents(documents):
  """TREC-1 to TREC-3 documents (TIPSTER volumes 1 and 2)"""
  return { "path": documents }

@FileDownloader(
  "topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.51-100.gz",
  transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1"))
)
@Dataset(TrecTopics, id="1.topics")
def trec1_topics(topics):
  return { "path": topics, "parts": ["desc"] }

@ConcatDownload(
  "assessments.qrels", "http://trec.nist.gov/data/qrels_eng/qrels.51-100.disk1.disk2.parts1-5.tar.gz",
  transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1"))
)
@Dataset(TrecAssessments, id="1.assessments")
def trec1_assessments(assessments):
  return { "path": assessments }

@Reference("documents", trec1_documents)
@Reference("topics", trec1_topics)
@Reference("assessments", trec1_assessments)
@Dataset(Adhoc, id="1")
def trec1(documents, topics, assessments):
  "Ad-hoc task of TREC 1 (1992)"
  return {
    "documents": documents,
    "topics": topics,
    "assessments": assessments
  }



# --- TREC 2 (1993)


@FileDownloader(
  "topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.101-150.gz",
  transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1"))
)
@Dataset(TrecTopics, id="2.topics")
def trec2_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@ConcatDownload(
  "assessments.qrels", "http://trec.nist.gov/data/qrels_eng/qrels.101-150.disk1.disk2.parts1-5.tar.gz",
  transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1"))
)
@Dataset(TrecAssessments, id="2.assessments")
def trec2_assessments(assessments):
  return { "path": assessments  }

@Reference("documents", trec1_documents)
@Reference("topics", trec2_topics)
@Reference("assessments", trec2_assessments)
@Dataset(Adhoc, id="2")
def trec2(documents, topics, assessments):
  "Ad-hoc task of TREC 2 (1993)"
  return {
    "documents": documents,
    "topics": topics,
    "assessments": assessments
  }




# --- TREC 3 (1994)


@FileDownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.151-200.gz")
@Dataset(TrecTopics, id="3.topics")
def trec3_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@ConcatDownload(
  "assessments.qrels", "http://trec.nist.gov/data/qrels_eng/qrels.151-200.201-250.disks1-3.all.tar.gz",
  transforms=TransformList(Gunzip(), Filter(r"^(1\d\d|200)\s"))
)
@Dataset(TrecAssessments, id="3.assessments")
def trec3_assessments(assessments):
  return { "path": assessments }

@Reference("documents", trec1_documents)
@Reference("topics", trec3_topics)
@Reference("assessments", trec3_assessments)
@Dataset(Adhoc, id="3")
def trec3(documents, topics, assessments):
  "Ad-hoc task of TREC 3 (1994)"
  return {
    "documents": documents,
    "topics": topics,
    "assessments": assessments
  }



# --- TREC 4 (1995)


@Links("documents",
  ap88=ap88.path, ap89=ap89.path, ap90=ap90.path,
  fr88=fr88.path,
  sjm1=sjm1.path,
  wsj90=wsj90.path, wsj91=wsj91.path, wsj92=wsj92.path,
  ziff2=ziff2.path, ziff3=ziff3.path)
@Dataset(TipsterCollection, id="4.documents")
def trec4_documents(documents):
  """TREC-4 documents"""
  return { "path": documents }

@FileDownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.201-250.gz")
@Dataset(TrecTopics, id="4.topics")
def trec4_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@ConcatDownload(
  "assessments.qrels", "http://trec.nist.gov/data/qrels_eng/qrels.201-250.disk2.disk3.parts1-5.tar.gz"
)
@Dataset(TrecAssessments, id="4.assessments")
def trec4_assessments(assessments):
  return { "path": assessments, "parts": ["desc"] }

@Reference("documents", trec4_documents)
@Reference("topics", trec4_topics)
@Reference("assessments", trec4_assessments)
@Dataset(Adhoc, id="4")
def trec4(documents, topics, assessments):
  "Ad-hoc task of TREC 4 (1995)"
  return {
    "documents": documents,
    "topics": topics,
    "assessments": assessments
  }



# --- TREC 5 (1995)

@Links("documents",
  ap88=ap88.path, 
  cr1=cr1.path, 
  fr88=fr88.path, fr94=fr94.path,
  ft1=ft1.path,
  wsj90=wsj90.path, wsj91=wsj91.path, wsj9=wsj92.path,
  ziff2=ziff2.path
)
@Dataset(TipsterCollection, id="4.documents")
def trec5_documents(documents):
  """TREC-5 documents"""
  return { "path": documents }

@FileDownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.251-300.gz")
@Dataset(TrecTopics, id="5.topics")
def trec5_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@ConcatDownload("assessments.qrels", url="http://trec.nist.gov/data/qrels_eng/qrels.251-300.parts1-5.tar.gz")
@Dataset(TrecAssessments, id="5.qrels")
def trec5_assessments(assessments):
  return { "path": assessments }

@Reference("documents", trec5_documents)
@Reference("topics", trec5_topics)
@Reference("assessments", trec5_assessments)
@Dataset(Adhoc, id="5")
def trec5(documents, topics, assessments):
  "Ad-hoc task of TREC 5 (1996)"
  return { "documents": documents, "topics": topics, "assessments": assessments }



# -- TREC 6 (1997)

@Links("documents",
  cr1=cr1.path, 
  fbis1=fbis1.path,
  fr94=fr94.path,
  ft1=ft1.path,
  la8990=la8990.path
)
@Dataset(TipsterCollection, id="4.documents")
def trec6_documents(documents):
  """TREC-5 documents"""
  return { "path": documents }

@FileDownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.301-350.gz")
@Dataset(TrecTopics, id="6.topics")
def trec6_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@ConcatDownload("assessments.qrels", url="http://trec.nist.gov/data/qrels_eng/qrels.trec6.adhoc.parts1-5.tar.gz")
@Dataset(TrecAssessments, id="6.qrels")
def trec6_assessments(assessments):
  return { "path": assessments }

@Reference("documents", trec6_documents)
@Reference("topics", trec6_topics)
@Reference("assessments", trec6_assessments)
@Dataset(Adhoc, id="6")
def trec6(documents, topics, assessments):
  "Ad-hoc task of TREC 6 (1997)"
  return { "documents": documents, "topics": topics, "assessments": assessments }



# --- TREC 7 (1998)

@Links("documents",
  fbis1=fbis1.path,
  fr94=fr94.path,
  ft1=ft1.path,
  la8990=la8990.path
)
@Dataset(TipsterCollection, id="4.documents")
def trec7_documents(documents):
  """TREC-7 documents"""
  return { "path": documents }


@FileDownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.351-400.gz")
@Dataset(TrecTopics, id="7.topics")
def trec7_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@ConcatDownload("assessments.qrels", url="http://trec.nist.gov/data/qrels_eng/qrels.trec7.adhoc.parts1-5.tar.gz")
@Dataset(TrecAssessments, id="7.qrels")
def trec7_assessments(assessments):
  return { "path": assessments }

@Reference("documents", trec7_documents)
@Reference("topics", trec7_topics)
@Reference("assessments", trec7_assessments)
@Dataset(Adhoc, id="7")
def trec7(documents, topics, assessments):
  "Ad-hoc task of TREC 3 (1994)"
  return { "documents": documents, "topics": topics, "assessments": assessments }




# --- TREC 8 (1999)

@FileDownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.401-450.gz")
@Dataset(TrecTopics, id="8.topics")
def trec8_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@ConcatDownload("assessments.qrels", url="https://trec.nist.gov/data/qrels_eng/qrels.trec8.adhoc.parts1-5.tar.gz")
@Dataset(TrecAssessments, id="8.qrels")
def trec8_assessments(assessments):
  return { "path": assessments }

@Reference("documents", trec7_documents)
@Reference("topics", trec8_topics)
@Reference("assessments", trec8_assessments)
@Dataset(Adhoc, id="8")
def trec8(documents, topics, assessments):
  "Ad-hoc task of TREC 8 (1999)"
  return { "documents": documents, "topics": topics, "assessments": assessments }

# --- TREC Robust (2004)

@FileDownloader("topics", "http://trec.nist.gov/data/robust/04.testset.gz")
@Dataset(TrecTopics, id="robust.2004.topics")
def robust2004_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@FileDownloader("assessments.qrels", "http://trec.nist.gov/data/robust/qrels.robust2004.txt")
@Dataset(TrecAssessments, id="robust.2004.qrels")
def robust2004_assessments(assessments):
  return { "path": assessments }

@Reference("documents", trec7_documents)
@Reference("topics", robust2004_topics)
@Reference("assessments", robust2004_assessments)
@Dataset(Adhoc, id="robust.2004")
def robust2004(documents, topics, assessments):
  "Ad-hoc task of TREC Robust (2004)"
  return { "documents": documents, "topics": topics, "assessments": assessments }


# --- TREC Robust (2005)

@FileDownloader("topics", "http://trec.nist.gov/data/robust/05/05.50.topics.txt")
@Dataset(TrecTopics, id="robust.2005.topics")
def robust2005_topics(topics):
  return { "path": topics, "parts": ["title", "desc"] }

@FileDownloader("assessments.qrels", url="http://trec.nist.gov/data/robust/05/TREC2005.qrels.txt")
@Dataset(TrecAssessments, id="robust.2005.qrels")
def robust2005_assessments(assessments):
  return { "path": assessments }

@Reference("documents", aquaint)
@Reference("topics", robust2005_topics)
@Reference("assessments", robust2005_assessments)
@Dataset(Adhoc, id="robust.2005")
def robust2005(documents, topics, assessments):
  "Ad-hoc task of TREC Robust (2005)"
  return { "documents": documents, "topics": topics, "assessments": assessments }
