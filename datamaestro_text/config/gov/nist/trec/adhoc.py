"""TREC AD-HOC datasets and tasks
"""

from datamaestro.data import Generic
from datamaestro.download import Reference
from datamaestro.download.single import FileDownloader, ConcatDownload
from datamaestro.download.links import Links
from datamaestro.stream import TransformList
from datamaestro.stream.compress import Gunzip
from datamaestro.stream.lines import Replace
from datamaestro.definitions import Data, Argument, Type, DataTasks, DataTags, Dataset

from datamaestro_text.data.trec import TipsterCollection, TrecTopics, TrecAssessments
from datamaestro_text.data.ir import Adhoc

from .tipster import *


# --- TREC 1 (1992)

@Links("documents", 
  ap88=ap88.path, ap89=ap89.path, fr88=fr88.path, fr89=fr89.path,
  wsj87=wsj87.path, wsj88=wsj88.path, wsj89=wsj89.path,
  wsj90=wsj90.path, wsj91=wsj91.path, wsj92=wsj92.path,
  ziff1=ziff1.path, ziff2=ziff2.path)
@Dataset(TipsterCollection, id="1.documents")
def trec1_documents(documents):
  """TREC-1 to TREC-3 documents (TIPSTER volumes 1 and 2)"""
  return { "path": documents.path }

@FileDownloader(
  "topics", "http://trec.nist.gov/data/topics_eng/topics.51-100.gz", 
  transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1"))
)
@Dataset(TrecTopics, id="1.topics")
def trec1_topics(topics):
  return { "path": topics.path, "parts": ["desc"] }

@ConcatDownload(
  "qrels", "http://trec.nist.gov/data/qrels_eng/qrels.51-100.disk1.disk2.parts1-5.tar.gz", 
  transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1"))
)
@Dataset(TrecAssessments, id="1.assessments")
def trec1_assessments(qrels):
  return { "path": qrels.path, "parts": ["desc"] }

@Reference("documents", trec1_documents)
@Reference("topics", trec1_topics)
@Reference("assessments", trec1_assessments)
@Dataset(Adhoc, id="1")
def trec1(documents, topics, assessments):
  "Ad-hoc task of TREC 1 (1992)"
  return { 
    "documents": documents.value,
    "topics": topics.value,
    "assessments": assessments.value
  }

# ---
# id: 1
# name: "Ad-hoc task of TREC 1 (1992)"
# type: ir:Adhoc
# testtopics: !dataset ".1.topics"
# documents: !dataset ".1.documents"
# assessments: !dataset ".1.qrels"
# ...




# ---
# id: 2.topics
# name: "TREC 2 topics"
# handler: trec.adhoc/topics
# properties:
#   parts: [title, desc]
# download:
#   handler: /single:File
#   url: "http://trec.nist.gov/data/topics_eng/topics.101-150.gz"
#   transforms:
#     - /compress:Gunzip
#     # To get matching strings between queries and assessments
#     - [ /stream:Replace, { repl: "Number: \\1", pattern: "Number:(\\s+)0" }]
# ...
# ---
# id: 2.qrels
# name: "TREC 2 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:Concat
#   transforms: [ /compress:Gunzip ]
#   url: "http://trec.nist.gov/data/qrels_eng/qrels.101-150.disk1.disk2.parts1-5.tar.gz"
# ...
# ---
# id: 2
# name: "Ad-hoc task of TREC 2 (1993)"
# handler: trec.adhoc/task
# documents: !dataset .1.documents
# topics: !dataset .2.topics
# assessments: !dataset .2.qrels
# type: ir:Adhoc
# ...
# ---
# id: 3.topics
# name: "TREC 3 topics"
# handler: trec.adhoc/topics
# properties:
#   parts: [title, desc]
# download: !@/single:File
#   url: "http://trec.nist.gov/data/topics_eng/topics.151-200.gz"
# ...
# ---
# id: 3.qrels
# name: "TREC 3 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:Concat
#   transforms: [ /compress:Gunzip, [ /filter, { pattern: "^(1\\d\\d|200)\\s" }] ]
#   url: "http://trec.nist.gov/data/qrels_eng/qrels.151-200.201-250.disks1-3.all.tar.gz"
# ...
# ---
# id: 3
# handler: trec.adhoc/task
# name: "Ad-hoc task of TREC 3 (1994)"
# documents: !dataset ".1.documents"
# topics: !dataset ".3.topics"
# assessments: !dataset ".3.qrels"
# ...



# ---
# id: 4.documents
# name: Data collection used in TREC-4
# url: https://catalog.ldc.upenn.edu/LDC93T3A
# download: !@/multiple:Datasets
#   ap88: !dataset tipster!ap88
#   ap89: !dataset tipster!ap89
#   ap90: !dataset tipster!ap90
#   fr88: !dataset tipster!fr88
#   sjm1: !dataset tipster!sjm1
#   wsj90: !dataset tipster!wsj90
#   wsj91: !dataset tipster!wsj91
#   wsj92: !dataset tipster!wsj92 
#   ziff2: !dataset tipster!ziff2
#   ziff3: !dataset tipster!ziff3
# ...
# ---
# id: 4.topics
# name: "TREC 4 topics"
# handler: trec.adhoc/topics
# properties:
#   parts: [title, desc]
# download:
#   handler: /single:File
#   url: "http://trec.nist.gov/data/topics_eng/topics.201-250.gz"
#   transforms:
#     - /compress:Gunzip
# ...
# ---
# id: 4.qrels
# name: "TREC 4 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:Concat
#   transforms: [ /compress:Gunzip ]
#   url: "http://trec.nist.gov/data/qrels_eng/qrels.201-250.disk2.disk3.parts1-5.tar.gz"
# ...
# ---
# id: 4
# handler: trec.adhoc/task
# name: "Ad-hoc task of TREC 4 (1995)"
# documents: !dataset ".4.documents"
# topics: !dataset ".4.topics"
# assessments: !dataset ".4.qrels"
# ...
# ---
# id: 5.documents
# name: Data collection used in TREC-5
# url: https://catalog.ldc.upenn.edu/LDC93T3A
# references: [
#   !dataset tipster!ap88, !dataset tipster!cr1, !dataset tipster!fr88, !dataset tipster!fr94, !dataset tipster!ft1, 
#   !dataset tipster!wsj90, !dataset tipster!wsj91, !dataset tipster!wsj92, !dataset tipster!ziff2
# ]
# ...
# ---
# id: "5.topics"
# name: "TREC 5 topics"
# handler: trec.adhoc/topics
# properties:
#   parts: [title, desc]
# download:
#   handler: /single:File
#   url: "http://trec.nist.gov/data/topics_eng/topics.251-300.gz"
#   transforms:
#     - /compress:Gunzip
# ...
# ---
# id: "5.qrels"
# name: "TREC 5 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:Concat
#   transforms: [ /compress:Gunzip ]
#   url: "http://trec.nist.gov/data/qrels_eng/qrels.251-300.parts1-5.tar.gz"
# ...
# ---
# id: 5
# handler: trec.adhoc/task
# name: "Ad-hoc task of TREC 5 (1996)"
# documents: !dataset ".5.documents"
# topics: !dataset ".5.topics"
# assessments: !dataset ".5.qrels"
# ...
# ---
# # -- TREC 6 (1997)
# id: 6.documents
# name: Data collection used in TREC-6
# url: https://catalog.ldc.upenn.edu/LDC93T3A
# download: !@/multiple:Datasets
#   cr1: !dataset tipster!cr1
#   fbis1: !dataset tipster!fbis1
#   fr94: !dataset tipster!fr94
#   ft1: !dataset tipster!ft1
#   la8990: !dataset tipster!la8990
# ...
# ---
# id: 6.topics
# name: "TREC 6 topics"
# handler: trec.adhoc/topics
# properties:
#   parts: [title, desc]
# download:
#   handler: /single:File
#   url: "http://trec.nist.gov/data/topics_eng/topics.301-350.gz"
#   transforms:
#     - /compress:Gunzip
# ...
# ---
# id: 6.qrels
# name: "TREC 6 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:Concat
#   transforms: [ /compress:Gunzip ]
#   url: "http://trec.nist.gov/data/qrels_eng/qrels.trec6.adhoc.parts1-5.tar.gz"
# ...
# ---
# id: 6
# handler: trec.adhoc/task
# name: "Ad-hoc task of TREC 6 (1997)"
# documents: !dataset ".6.documents"
# topics: !dataset ".6.topics"
# assessments: !dataset ".6.qrels"


# # --- TREC 7 (1998)

# ...
# ---
# id: 7.documents
# url: https://catalog.ldc.upenn.edu/LDC93T3A
# name: Data collection used in TREC-7 and TREC-8
# download: !@/multiple:Datasets
#   fbis1: !dataset tipster!fbis1
#   fr94: !dataset tipster!fr94
#   ft1: !dataset tipster!ft1
#   la8990: !dataset tipster!la8990
# ...
# ---
# id: "7.topics"
# name: "TREC 7 topics"
# handler: trec.adhoc/topics
# properties:
#   parts: [title, desc]
# download:
#   handler: /single:File
#   url: "http://trec.nist.gov/data/topics_eng/topics.351-400.gz"
#   transforms:
#     - /compress:Gunzip
# ...
# ---
# id: "7.qrels"
# name: "TREC 7 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:Concat
#   transforms: [ /compress:Gunzip ]
#   url: "http://trec.nist.gov/data/qrels_eng/qrels.trec7.adhoc.parts1-5.tar.gz"
# ...
# ---
# id: 7
# handler: trec.adhoc/task
# name: "Ad-hoc task of TREC 3 (1994)"
# documents: !dataset ".7.documents"
# topics: !dataset ".4.topics"
# assessments: !dataset ".4.qrels"
# ...


# # --- TREC 8 (1999)

# ---
# id: "8.topics"
# name: "TREC 8 topics"
# handler: trec.adhoc/topics
# properties:
#   parts: [title, desc]
# download:
#   handler: /single:File
#   url: "http://trec.nist.gov/data/topics_eng/topics.401-450.gz"
#   transforms:
#     - /compress:Gunzip
# ...
# ---
# id: "8.qrels"
# name: "TREC 8 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:Concat
#   transforms: [ /compress:Gunzip ]
#   url: "http://trec.nist.gov/data/qrels_eng/qrels.trec8.adhoc.parts1-5.tar.gz"

# ...
# ---
# id: 8
# handler: trec.adhoc/task
# name: "Ad-hoc task of TREC 8 (1999)"
# documents: !dataset ".7.documents"
# topics: !dataset ".4.topics"
# assessments: !dataset ".4.qrels"


# # --- TREC Robust (2004)
# ...
# ---
# id: "robust.2004.topics"
# name: "TREC Robust 2004 topics"
# handler: trec.adhoc/topics
# download:
#   handler: /single:File
#   url: "http://trec.nist.gov/data/robust/04.testset.gz"
#   transforms: [ /compress:Gunzip ]
# ...
# ---
# id: "robust.2004.qrels"
# name: "TREC Robust 2004 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:File
#   url: "http://trec.nist.gov/data/robust/qrels.robust2004.txt"
# ...
# ---
# id: "robust.2004"
# handler: trec.adhoc/task
# name: "Ad-hoc task of TREC Robust (2004)"
# documents: !dataset ".7.documents"
# topics: !dataset ".robust.2004.topics"
# assessments: !dataset ".robust.2004.qrels"



# # --- TREC Robust (2005)
# ...
# ---
# id: "robust.2005.topics"
# name: "TREC Robust 2005 topics"
# handler: trec.adhoc/topics
# download:
#   handler: /single:File
#   url: "http://trec.nist.gov/data/robust/05/05.50.topics.txt"
# ...
# ---
# id: "robust.2005.qrels"
# name: "TREC Robust 2005 relevance assessments"
# handler: trec.adhoc/assessments
# download: !@/single:Concat
#   transforms: [ /compress:Gunzip ]
#   url: "http://trec.nist.gov/data/robust/05/TREC2005.qrels.txt"
# ...
# ---
# id: robust.2005
# handler: trec.adhoc/task
# name: "Ad-hoc task of TREC Robust (2005)"
# documents: !dataset "edu.upenn.ldc.aquaint"
# topics: !dataset ".robust.2005.topics"
# assessments: !dataset ".robust.2005.qrels"

