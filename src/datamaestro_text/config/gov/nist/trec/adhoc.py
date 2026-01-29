"""TREC Adhoc datasets and tasks

See [https://trec.nist.gov/data/test_coll.html](https://trec.nist.gov/data/test_coll.html)
"""

from datamaestro.download import reference
from datamaestro.download.single import FileDownloader, ConcatDownloader
from datamaestro.download.links import links
from datamaestro.stream import TransformList
from datamaestro.stream.compress import Gunzip
from datamaestro.stream.lines import Replace, Filter
from datamaestro.definitions import dataset

from datamaestro_text.data.ir.trec import (
    TipsterCollection,
    TrecTopics,
    TrecAdhocAssessments,
)
from datamaestro_text.data.ir import Adhoc

from . import tipster
from datamaestro_text.config.edu.upenn.ldc.aquaint import Aquaint


# --- TREC 1 (1992)


@dataset(id="1.documents")
class Trec1Documents(TipsterCollection):
    """TREC-1 to TREC-3 documents (TIPSTER volumes 1 and 2)"""

    DOCUMENTS = links(
        "documents",
        ap88=tipster.Ap88,
        ap89=tipster.Ap89,
        fr88=tipster.Fr88,
        fr89=tipster.Fr89,
        wsj87=tipster.Wsj87,
        wsj88=tipster.Wsj88,
        wsj89=tipster.Wsj89,
        wsj90=tipster.Wsj90,
        wsj91=tipster.Wsj91,
        wsj92=tipster.Wsj92,
        ziff1=tipster.Ziff1,
        ziff2=tipster.Ziff2,
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DOCUMENTS.path)


@dataset(id="1.topics", url="")
class Trec1Topics(TrecTopics):
    FILE = FileDownloader(
        "topics.sgml",
        "http://trec.nist.gov/data/topics_eng/topics.51-100.gz",
        transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1")),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["desc"])


@dataset(id="1.assessments")
class Trec1Assessments(TrecAdhocAssessments):
    FILE = ConcatDownloader(
        "assessments.qrels",
        "http://trec.nist.gov/data/qrels_eng/qrels.51-100.disk1.disk2.parts1-5.tar.gz",
        transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1")),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="1")
class Trec1(Adhoc):
    "Ad-hoc task of TREC 1 (1992)"

    DOCUMENTS = reference(varname="documents", reference=Trec1Documents)
    TOPICS = reference(varname="topics", reference=Trec1Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Trec1Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# --- TREC 2 (1993)


@dataset(id="2.topics")
class Trec2Topics(TrecTopics):
    FILE = FileDownloader(
        "topics.sgml",
        "http://trec.nist.gov/data/topics_eng/topics.101-150.gz",
        transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1")),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="2.assessments")
class Trec2Assessments(TrecAdhocAssessments):
    FILE = ConcatDownloader(
        "assessments.qrels",
        "http://trec.nist.gov/data/qrels_eng/qrels.101-150.disk1.disk2.parts1-5.tar.gz",
        transforms=TransformList(Gunzip(), Replace(r"Number:(\s+)0", r"Number: \1")),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="2")
class Trec2(Adhoc):
    "Ad-hoc task of TREC 2 (1993)"

    DOCUMENTS = reference(varname="documents", reference=Trec1Documents)
    TOPICS = reference(varname="topics", reference=Trec2Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Trec2Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# --- TREC 3 (1994)


@dataset(id="3.topics")
class Trec3Topics(TrecTopics):
    FILE = FileDownloader(
        "topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.151-200.gz"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="3.assessments")
class Trec3Assessments(TrecAdhocAssessments):
    FILE = ConcatDownloader(
        "assessments.qrels",
        "http://trec.nist.gov/data/qrels_eng/qrels.151-200.201-250.disks1-3.all.tar.gz",
        transforms=TransformList(Gunzip(), Filter(r"^(1\d\d|200)\s")),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="3")
class Trec3(Adhoc):
    "Ad-hoc task of TREC 3 (1994)"

    DOCUMENTS = reference(varname="documents", reference=Trec1Documents)
    TOPICS = reference(varname="topics", reference=Trec3Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Trec3Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# --- TREC 4 (1995)


@dataset(id="4.documents")
class Trec4Documents(TipsterCollection):
    """TREC-4 documents"""

    DOCUMENTS = links(
        "documents",
        ap88=tipster.Ap88,
        ap89=tipster.Ap89,
        ap90=tipster.Ap90,
        fr88=tipster.Fr88,
        sjm1=tipster.Sjm1,
        wsj90=tipster.Wsj90,
        wsj91=tipster.Wsj91,
        wsj92=tipster.Wsj92,
        ziff2=tipster.Ziff2,
        ziff3=tipster.Ziff3,
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DOCUMENTS.path)


@dataset(id="4.topics")
class Trec4Topics(TrecTopics):
    FILE = FileDownloader(
        "topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.201-250.gz"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="4.assessments")
class Trec4Assessments(TrecAdhocAssessments):
    FILE = ConcatDownloader(
        "assessments.qrels",
        "http://trec.nist.gov/data/qrels_eng/qrels.201-250.disk2.disk3.parts1-5.tar.gz",
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="4")
class Trec4(Adhoc):
    "Ad-hoc task of TREC 4 (1995)"

    DOCUMENTS = reference(varname="documents", reference=Trec4Documents)
    TOPICS = reference(varname="topics", reference=Trec4Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Trec4Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# --- TREC 5 (1995)


@dataset(id="5.documents")
class Trec5Documents(TipsterCollection):
    """TREC-5 documents"""

    DOCUMENTS = links(
        "documents",
        ap88=tipster.Ap88,
        cr1=tipster.Cr1,
        fr88=tipster.Fr88,
        fr94=tipster.Fr94,
        ft1=tipster.Ft1,
        wsj90=tipster.Wsj90,
        wsj91=tipster.Wsj91,
        wsj9=tipster.Wsj92,
        ziff2=tipster.Ziff2,
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DOCUMENTS.path)


@dataset(id="5.topics")
class Trec5Topics(TrecTopics):
    FILE = FileDownloader(
        "topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.251-300.gz"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="5.qrels")
class Trec5Assessments(TrecAdhocAssessments):
    FILE = ConcatDownloader(
        "assessments.qrels",
        url="http://trec.nist.gov/data/qrels_eng/qrels.251-300.parts1-5.tar.gz",
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="5")
class Trec5(Adhoc):
    "Ad-hoc task of TREC 5 (1996)"

    DOCUMENTS = reference(varname="documents", reference=Trec5Documents)
    TOPICS = reference(varname="topics", reference=Trec5Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Trec5Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# -- TREC 6 (1997)


@dataset(id="6.documents")
class Trec6Documents(TipsterCollection):
    """TREC-5 documents"""

    DOCUMENTS = links(
        "documents",
        cr1=tipster.Cr1,
        fbis1=tipster.Fbis1,
        fr94=tipster.Fr94,
        ft1=tipster.Ft1,
        la8990=tipster.La8990,
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DOCUMENTS.path)


@dataset(id="6.topics")
class Trec6Topics(TrecTopics):
    FILE = FileDownloader(
        "topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.301-350.gz"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="6.qrels")
class Trec6Assessments(TrecAdhocAssessments):
    FILE = ConcatDownloader(
        "assessments.qrels",
        url="http://trec.nist.gov/data/qrels_eng/qrels.trec6.adhoc.parts1-5.tar.gz",
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="6")
class Trec6(Adhoc):
    "Ad-hoc task of TREC 6 (1997)"

    DOCUMENTS = reference(varname="documents", reference=Trec6Documents)
    TOPICS = reference(varname="topics", reference=Trec6Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Trec6Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# --- TREC 7 (1998)


@dataset(id="7.documents")
class Trec7Documents(TipsterCollection):
    """TREC-7 documents"""

    DOCUMENTS = links(
        "documents",
        fbis1=tipster.Fbis1,
        fr94=tipster.Fr94,
        ft1=tipster.Ft1,
        la8990=tipster.La8990,
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DOCUMENTS.path)


@dataset(id="7.topics")
class Trec7Topics(TrecTopics):
    FILE = FileDownloader(
        "topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.351-400.gz"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="7.qrels")
class Trec7Assessments(TrecAdhocAssessments):
    FILE = ConcatDownloader(
        "assessments.qrels",
        url="http://trec.nist.gov/data/qrels_eng/qrels.trec7.adhoc.parts1-5.tar.gz",
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="7")
class Trec7(Adhoc):
    "Ad-hoc task of TREC 3 (1994)"

    DOCUMENTS = reference(varname="documents", reference=Trec7Documents)
    TOPICS = reference(varname="topics", reference=Trec7Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Trec7Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# --- TREC 8 (1999)


@dataset(id="8.topics")
class Trec8Topics(TrecTopics):
    FILE = FileDownloader(
        "topics.sgml", "http://trec.nist.gov/data/topics_eng/topics.401-450.gz"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="8.qrels")
class Trec8Assessments(TrecAdhocAssessments):
    FILE = ConcatDownloader(
        "assessments.qrels",
        url="https://trec.nist.gov/data/qrels_eng/qrels.trec8.adhoc.parts1-5.tar.gz",
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="8")
class Trec8(Adhoc):
    "Ad-hoc task of TREC 8 (1999)"

    DOCUMENTS = reference(varname="documents", reference=Trec7Documents)
    TOPICS = reference(varname="topics", reference=Trec8Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Trec8Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# --- TREC Robust (2004)


@dataset(id="robust.2004.topics")
class Robust2004Topics(TrecTopics):
    FILE = FileDownloader("topics", "http://trec.nist.gov/data/robust/04.testset.gz")

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="robust.2004.qrels")
class Robust2004Assessments(TrecAdhocAssessments):
    FILE = FileDownloader(
        "assessments.qrels", "http://trec.nist.gov/data/robust/qrels.robust2004.txt"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="robust.2004")
class Robust2004(Adhoc):
    "Ad-hoc task of TREC Robust (2004)"

    DOCUMENTS = reference(varname="documents", reference=Trec7Documents)
    TOPICS = reference(varname="topics", reference=Robust2004Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Robust2004Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )


# --- TREC Robust (2005)


@dataset(id="robust.2005.topics")
class Robust2005Topics(TrecTopics):
    FILE = FileDownloader(
        "topics", "http://trec.nist.gov/data/robust/05/05.50.topics.txt"
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path, parts=["title", "desc"])


@dataset(id="robust.2005.qrels")
class Robust2005Assessments(TrecAdhocAssessments):
    FILE = FileDownloader(
        "assessments.qrels",
        url="http://trec.nist.gov/data/robust/05/TREC2005.qrels.txt",
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.FILE.path)


@dataset(id="robust.2005")
class Robust2005(Adhoc):
    "Ad-hoc task of TREC Robust (2005)"

    DOCUMENTS = reference(varname="documents", reference=Aquaint)
    TOPICS = reference(varname="topics", reference=Robust2005Topics)
    ASSESSMENTS = reference(varname="assessments", reference=Robust2005Assessments)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.DOCUMENTS.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.ASSESSMENTS.prepare(),
        )
