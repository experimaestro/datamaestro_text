"""TREC AD-HOC datasets and tasks

https://trec.nist.gov/data/test_coll.html
"""

from datamaestro.download import reference
from datamaestro.download.single import filedownloader, concatdownload
from datamaestro.download.links import links
from datamaestro.stream import TransformList
from datamaestro.stream.compress import Gunzip
from datamaestro.stream.lines import Replace, Filter
from datamaestro.definitions import dataset

from datamaestro_text.data.ir.trec import (
    TipsterCollection,
    TrecAdhocTopics,
    TrecAdhocAssessments,
)
from datamaestro_text.data.ir import Adhoc

from . import tipster
from datamaestro_text.config.edu.upenn.ldc.aquaint import aquaint


# --- TREC 1 (1992)


@links(
    "documents",
    ap88=tipster.ap88.path,
    ap89=tipster.ap89.path,
    fr88=tipster.fr88.path,
    fr89=tipster.fr89.path,
    wsj87=tipster.wsj87.path,
    wsj88=tipster.wsj88.path,
    wsj89=tipster.wsj89.path,
    wsj90=tipster.wsj90.path,
    wsj91=tipster.wsj91.path,
    wsj92=tipster.wsj92.path,
    ziff1=tipster.ziff1.path,
    ziff2=tipster.ziff2.path,
)
@dataset(TipsterCollection, id="1.documents")
def trec1_documents(documents):
    """TREC-1 to TREC-3 documents (TIPSTER volumes 1 and 2)"""
    return {"path": documents}


@filedownloader(
    "topics.sgml",
    "http://trec.nist.gov/data/topics_eng/topics.51-100.gz",
    transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1")),
)
@dataset(TrecAdhocTopics, id="1.topics", url="")
def trec1_topics(topics):
    return {"path": topics, "parts": ["desc"]}


@concatdownload(
    "assessments.qrels",
    "http://trec.nist.gov/data/qrels_eng/qrels.51-100.disk1.disk2.parts1-5.tar.gz",
    transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1")),
)
@dataset(TrecAdhocAssessments, id="1.assessments")
def trec1_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec1_documents)
@reference("topics", trec1_topics)
@reference("assessments", trec1_assessments)
@dataset(Adhoc, id="1")
def trec1(documents, topics, assessments):
    "Ad-hoc task of TREC 1 (1992)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# --- TREC 2 (1993)


@filedownloader(
    "topics.sgml",
    "http://trec.nist.gov/data/topics_eng/topics.101-150.gz",
    transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1")),
)
@dataset(TrecAdhocTopics, id="2.topics")
def trec2_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@concatdownload(
    "assessments.qrels",
    "http://trec.nist.gov/data/qrels_eng/qrels.101-150.disk1.disk2.parts1-5.tar.gz",
    transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1")),
)
@dataset(TrecAdhocAssessments, id="2.assessments")
def trec2_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec1_documents)
@reference("topics", trec2_topics)
@reference("assessments", trec2_assessments)
@dataset(Adhoc, id="2")
def trec2(documents, topics, assessments):
    "Ad-hoc task of TREC 2 (1993)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# --- TREC 3 (1994)


@filedownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.151-200.gz")
@dataset(TrecAdhocTopics, id="3.topics")
def trec3_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@concatdownload(
    "assessments.qrels",
    "http://trec.nist.gov/data/qrels_eng/qrels.151-200.201-250.disks1-3.all.tar.gz",
    transforms=TransformList(Gunzip(), Filter(r"^(1\d\d|200)\s")),
)
@dataset(TrecAdhocAssessments, id="3.assessments")
def trec3_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec1_documents)
@reference("topics", trec3_topics)
@reference("assessments", trec3_assessments)
@dataset(Adhoc, id="3")
def trec3(documents, topics, assessments):
    "Ad-hoc task of TREC 3 (1994)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# --- TREC 4 (1995)


@links(
    "documents",
    ap88=tipster.ap88.path,
    ap89=tipster.ap89.path,
    ap90=tipster.ap90.path,
    fr88=tipster.fr88.path,
    sjm1=tipster.sjm1.path,
    wsj90=tipster.wsj90.path,
    wsj91=tipster.wsj91.path,
    wsj92=tipster.wsj92.path,
    ziff2=tipster.ziff2.path,
    ziff3=tipster.ziff3.path,
)
@dataset(TipsterCollection, id="4.documents")
def trec4_documents(documents):
    """TREC-4 documents"""
    return {"path": documents}


@filedownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.201-250.gz")
@dataset(TrecAdhocTopics, id="4.topics")
def trec4_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@concatdownload(
    "assessments.qrels",
    "http://trec.nist.gov/data/qrels_eng/qrels.201-250.disk2.disk3.parts1-5.tar.gz",
)
@dataset(TrecAdhocAssessments, id="4.assessments")
def trec4_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec4_documents)
@reference("topics", trec4_topics)
@reference("assessments", trec4_assessments)
@dataset(Adhoc, id="4")
def trec4(documents, topics, assessments):
    "Ad-hoc task of TREC 4 (1995)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# --- TREC 5 (1995)


@links(
    "documents",
    ap88=tipster.ap88.path,
    cr1=tipster.cr1.path,
    fr88=tipster.fr88.path,
    fr94=tipster.fr94.path,
    ft1=tipster.ft1.path,
    wsj90=tipster.wsj90.path,
    wsj91=tipster.wsj91.path,
    wsj9=tipster.wsj92.path,
    ziff2=tipster.ziff2.path,
)
@dataset(TipsterCollection, id="5.documents")
def trec5_documents(documents):
    """TREC-5 documents"""
    return {"path": documents}


@filedownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.251-300.gz")
@dataset(TrecAdhocTopics, id="5.topics")
def trec5_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@concatdownload(
    "assessments.qrels",
    url="http://trec.nist.gov/data/qrels_eng/qrels.251-300.parts1-5.tar.gz",
)
@dataset(TrecAdhocAssessments, id="5.qrels")
def trec5_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec5_documents)
@reference("topics", trec5_topics)
@reference("assessments", trec5_assessments)
@dataset(Adhoc, id="5")
def trec5(documents, topics, assessments):
    "Ad-hoc task of TREC 5 (1996)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# -- TREC 6 (1997)


@links(
    "documents",
    cr1=tipster.cr1.path,
    fbis1=tipster.fbis1.path,
    fr94=tipster.fr94.path,
    ft1=tipster.ft1.path,
    la8990=tipster.la8990.path,
)
@dataset(TipsterCollection, id="6.documents")
def trec6_documents(documents):
    """TREC-5 documents"""
    return {"path": documents}


@filedownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.301-350.gz")
@dataset(TrecAdhocTopics, id="6.topics")
def trec6_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@concatdownload(
    "assessments.qrels",
    url="http://trec.nist.gov/data/qrels_eng/qrels.trec6.adhoc.parts1-5.tar.gz",
)
@dataset(TrecAdhocAssessments, id="6.qrels")
def trec6_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec6_documents)
@reference("topics", trec6_topics)
@reference("assessments", trec6_assessments)
@dataset(Adhoc, id="6")
def trec6(documents, topics, assessments):
    "Ad-hoc task of TREC 6 (1997)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# --- TREC 7 (1998)


@links(
    "documents",
    fbis1=tipster.fbis1.path,
    fr94=tipster.fr94.path,
    ft1=tipster.ft1.path,
    la8990=tipster.la8990.path,
)
@dataset(TipsterCollection, id="7.documents")
def trec7_documents(documents):
    """TREC-7 documents"""
    return {"path": documents}


@filedownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.351-400.gz")
@dataset(TrecAdhocTopics, id="7.topics")
def trec7_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@concatdownload(
    "assessments.qrels",
    url="http://trec.nist.gov/data/qrels_eng/qrels.trec7.adhoc.parts1-5.tar.gz",
)
@dataset(TrecAdhocAssessments, id="7.qrels")
def trec7_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec7_documents)
@reference("topics", trec7_topics)
@reference("assessments", trec7_assessments)
@dataset(Adhoc, id="7")
def trec7(documents, topics, assessments):
    "Ad-hoc task of TREC 3 (1994)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# --- TREC 8 (1999)


@filedownloader("topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.401-450.gz")
@dataset(TrecAdhocTopics, id="8.topics")
def trec8_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@concatdownload(
    "assessments.qrels",
    url="https://trec.nist.gov/data/qrels_eng/qrels.trec8.adhoc.parts1-5.tar.gz",
)
@dataset(TrecAdhocAssessments, id="8.qrels")
def trec8_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec7_documents)
@reference("topics", trec8_topics)
@reference("assessments", trec8_assessments)
@dataset(Adhoc, id="8")
def trec8(documents, topics, assessments):
    "Ad-hoc task of TREC 8 (1999)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# --- TREC Robust (2004)


@filedownloader("topics", "http://trec.nist.gov/data/robust/04.testset.gz")
@dataset(TrecAdhocTopics, id="robust.2004.topics")
def robust2004_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@filedownloader(
    "assessments.qrels", "http://trec.nist.gov/data/robust/qrels.robust2004.txt"
)
@dataset(TrecAdhocAssessments, id="robust.2004.qrels")
def robust2004_assessments(assessments):
    return {"path": assessments}


@reference("documents", trec7_documents)
@reference("topics", robust2004_topics)
@reference("assessments", robust2004_assessments)
@dataset(Adhoc, id="robust.2004")
def robust2004(documents, topics, assessments):
    "Ad-hoc task of TREC Robust (2004)"
    return {"documents": documents, "topics": topics, "assessments": assessments}


# --- TREC Robust (2005)


@filedownloader("topics", "http://trec.nist.gov/data/robust/05/05.50.topics.txt")
@dataset(TrecAdhocTopics, id="robust.2005.topics")
def robust2005_topics(topics):
    return {"path": topics, "parts": ["title", "desc"]}


@filedownloader(
    "assessments.qrels", url="http://trec.nist.gov/data/robust/05/TREC2005.qrels.txt"
)
@dataset(TrecAdhocAssessments, id="robust.2005.qrels")
def robust2005_assessments(assessments):
    return {"path": assessments}


@reference("documents", aquaint)
@reference("topics", robust2005_topics)
@reference("assessments", robust2005_assessments)
@dataset(Adhoc, id="robust.2005")
def robust2005(documents, topics, assessments):
    "Ad-hoc task of TREC Robust (2005)"
    return {"documents": documents, "topics": topics, "assessments": assessments}
