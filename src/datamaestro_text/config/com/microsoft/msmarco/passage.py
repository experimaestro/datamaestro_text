"""MS MARCO (Microsoft Machine Reading Comprehension) is a large scale dataset focused on machine reading comprehension, question answering, and passage ranking. A variant of this task will be the part of TREC and AFIRM 2019. For Updates about TREC 2019 please follow This Repository Passage Reranking task Task Given a query q and a the 1000 most relevant passages P = p1, p2, p3,... p1000, as retrieved by BM25 a succeful system is expected to rerank the most relevant passage as high as possible. For this task not all 1000 relevant items have a human labeled relevant passage. Evaluation will be done using MRR.

**Publication**:
Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, RanganMajumder, and Li Deng. 2016.
MS MARCO: A Human Generated MAchineReading COmprehension Dataset. In CoCo@NIPS.


See [https://github.com/microsoft/MSMARCO-Passage-Ranking](https://github.com/microsoft/MSMARCO-Passage-Ranking) for more details
"""

from datamaestro.annotations.agreement import useragreement
from datamaestro.data import Folder
from datamaestro.download.single import FileDownloader
from datamaestro.download import reference
from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.download.archive import TarDownloader
from datamaestro_text.data.ir import RerankAdhoc, Adhoc, TrainingTripletsLines
from datamaestro_text.data.ir.csv import (
    Topics,
    AdhocRunWithText,
    Documents,
)
from datamaestro_text.data.ir.trec import TrecAdhocAssessments
from datamaestro.utils import HashCheck
from hashlib import md5


# User agreement
lua = useragreement(
    """Will begin downloading MS-MARCO dataset.
Please confirm you agree to the authors' data usage stipulations found at
http://www.msmarco.org/dataset.aspx""",
    id="net.windows.msmarco",
)

# --- Document collection


# TODO: Not ideal since it would be better to have small versions right away
# instead of downloading again the MS Marco Collection
@lua
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class CollectionEtc(Folder):
    """Documents and some more files"""

    DATA = TarDownloader(
        "data",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/collectionandqueries.tar.gz",
        checker=HashCheck("31644046b18952c1386cd4564ba2ae69", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return Folder.C(path=cls.DATA.path)


@lua
@dataset(size="2.9GB")
class Collection(Documents):
    """MS-Marco documents

    This file contains each passage in the larger MSMARCO dataset.

    Format is TSV (PID \\t Passage)"""

    DATA = reference(varname="data", reference=CollectionEtc)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DATA.prepare().path / "collection.tsv")


# --- Train


@lua
@dataset(size="2.5GB")
class TrainRun(AdhocRunWithText):
    """

    TSV format: qid, pid, query, passage
    """

    RUN = TarDownloader(
        "run",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.train.tar.gz",
        checker=HashCheck("d99fdbd5b2ea84af8aa23194a3263052", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.RUN.path / "top1000.train.tsv")


@lua
@dataset()
class TrainQueries(Topics):
    QUERIES = TarDownloader(
        "queries",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz",
        files=["queries.train.tsv"],
        checker=HashCheck("c177b2795d5f2dcc524cf00fcd973be1", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.QUERIES.path / "queries.train.tsv")


@lua
@dataset(size="10.1MB")
class TrainQrels(TrecAdhocAssessments):
    QRELS = FileDownloader(
        "qrels.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/qrels.train.tsv",
        checker=HashCheck("733fb9fe12d93e497f7289409316eccf", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.QRELS.path)


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class Train(Adhoc):
    """MS-Marco train dataset"""

    COLLECTION = reference(varname="collection", reference=Collection)
    TOPICS = reference(varname="topics", reference=TrainQueries)
    QRELS = reference(varname="qrels", reference=TrainQrels)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.COLLECTION.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.QRELS.prepare(),
        )


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class TrainWithrun(RerankAdhoc):
    """MSMarco train dataset, including the top-1000 to documents to re-rank"""

    TRAIN = reference(varname="train", reference=Train)
    RUN = reference(varname="run", reference=TrainRun)

    @classmethod
    def __create_dataset__(cls, dataset):
        train = cls.TRAIN.prepare()
        return cls.C(**train.__arguments__(), run=cls.RUN.prepare())


# Training triplets


@dataset(
    url="https://github.com/microsoft/MSMARCO-Passage-Ranking",
    size="5.7GB",
)
class TrainIdtriples(TrainingTripletsLines):
    """Full training triples (query, positive passage, negative passage) with IDs"""

    TRIPLES = FileDownloader(
        "triples.tsv",
        size=1_841_693_309,
        url="https://msmarco.blob.core.windows.net/msmarcoranking/qidpidtriples.train.full.2.tsv.gz",
        checker=HashCheck("4e58f45f82f3fe99e3239ecffd8ed371", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.TRIPLES.path, doc_ids=True, topic_ids=True)


@dataset(
    url="https://github.com/microsoft/MSMARCO-Passage-Ranking",
    size="27.1GB",
)
class TrainTexttriplesSmall(TrainingTripletsLines):
    """Small training triples (query, positive passage, negative passage) with text"""

    TRIPLES = FileDownloader(
        "triples.tsv",
        size=7_930_881_353,
        url="https://msmarco.blob.core.windows.net/msmarcoranking/triples.train.small.tar.gz",
        checker=HashCheck("c13bf99ff23ca691105ad12eab837f84", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.TRIPLES.path)


@dataset(
    url="https://github.com/microsoft/MSMARCO-Passage-Ranking",
    size="272.2GB",
)
class TrainTexttripleFull(TrainingTripletsLines):
    """Full training triples (query, positive passage, negative passage) with text"""

    TRIPLES = FileDownloader(
        "triples.tsv",
        size=77_877_731_328,
        url="https://msmarco.blob.core.windows.net/msmarcoranking/triples.train.full.tar.gz",
        checker=HashCheck("8d509d484ea1971e792b812ae4800c6f", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.TRIPLES.path)


# ---
# --- Development set
# ---


@lua
@dataset()
class DevQueries(Topics):
    QUERIES = TarDownloader(
        "queries",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz",
        files=["queries.dev.tsv"],
        checker=HashCheck("c177b2795d5f2dcc524cf00fcd973be1", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.QUERIES.path / "queries.dev.tsv")


@lua
@dataset()
class DevRun(AdhocRunWithText):
    RUN = TarDownloader(
        "run",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.dev.tar.gz",
        checker=HashCheck("8c140662bdf123a98fbfe3bb174c5831", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.RUN.path / "top1000.eval.tsv")


@lua
@dataset()
class DevQrels(TrecAdhocAssessments):
    QRELS = FileDownloader(
        "qrels.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/qrels.dev.tsv",
        checker=HashCheck("9157ccaeaa8227f91722ba5770787b16", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.QRELS.path)


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class Dev(Adhoc):
    """MS-Marco dev dataset"""

    COLLECTION = reference(varname="collection", reference=Collection)
    TOPICS = reference(varname="topics", reference=DevQueries)
    QRELS = reference(varname="qrels", reference=DevQrels)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.COLLECTION.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.QRELS.prepare(),
        )


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class DevWithrun(RerankAdhoc):
    """MSMarco dev dataset, including the top-1000 to documents to re-rank"""

    DEV = reference(varname="dev", reference=Dev)
    RUN = reference(varname="run", reference=DevRun)

    @classmethod
    def __create_dataset__(cls, dataset):
        dev = cls.DEV.prepare()
        return cls.C(**dev.__arguments__(), run=cls.RUN.prepare())


@lua
@dataset()
class EvalWithrun(AdhocRunWithText):
    RUN = TarDownloader(
        "run",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.eval.tar.gz",
        checker=HashCheck("73778cd99f6e0632d12d0b5731b20a02", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.RUN.path / "top1000.eval.tsv")


# ---
# --- Relevant Passages
# --- https://github.com/microsoft/MSMARCO-Passage-Ranking#relevant-passages
# ---


@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class DevSmallQueries(Topics):
    DATA = reference(varname="data", reference=CollectionEtc)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DATA.prepare().path / "queries.dev.small.tsv")


@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class DevSmallQrels(TrecAdhocAssessments):
    DATA = reference(varname="data", reference=CollectionEtc)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DATA.prepare().path / "qrels.dev.small.tsv")


@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class DevSmall(Adhoc):
    TOPICS = reference(varname="topics", reference=DevSmallQueries)
    QRELS = reference(varname="qrels", reference=DevSmallQrels)
    COLLECTION = reference(varname="collection", reference=Collection)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.COLLECTION.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.QRELS.prepare(),
        )


@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class EvalQueriesSmall(Topics):
    DATA = reference(varname="data", reference=CollectionEtc)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.DATA.prepare().path / "queries.eval.small.tsv")


# ---
# --- TREC 2019
# ---


@lua
@dataset()
class Trec2019TestQueries(Topics):
    QUERIES = FileDownloader(
        "queries.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-test2019-queries.tsv.gz",
        checker=HashCheck("756e60d714cee28d3b552289d6272f1d", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.QUERIES.path)


@lua
@dataset()
class Trec2019TestRun(AdhocRunWithText):
    RUN = FileDownloader(
        "run.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-passagetest2019-top1000.tsv.gz",
        checker=HashCheck("ec9e012746aa9763c7ff10b3336a3ce1", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.RUN.path / "top1000.eval.tsv")


@lua
@dataset()
class Trec2019TestQrels(TrecAdhocAssessments):
    QRELS = FileDownloader(
        "qrels.tsv",
        url="https://trec.nist.gov/data/deep/2019qrels-pass.txt",
        checker=HashCheck("2f4be390198da108f6845c822e5ada14", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.QRELS.path)


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://microsoft.github.io/msmarco/TREC-Deep-Learning-2019.html")
class Trec2019Test(Adhoc):
    "TREC Deep Learning (2019)"

    COLLECTION = reference(varname="collection", reference=Collection)
    TOPICS = reference(varname="topics", reference=Trec2019TestQueries)
    QRELS = reference(varname="qrels", reference=Trec2019TestQrels)

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(
            documents=cls.COLLECTION.prepare(),
            topics=cls.TOPICS.prepare(),
            assessments=cls.QRELS.prepare(),
        )


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://microsoft.github.io/msmarco/TREC-Deep-Learning-2019.html")
class Trec2019TestWithrun(RerankAdhoc):
    """TREC Deep Learning (2019), including the top-1000 to documents to re-rank"""

    TREC2019 = reference(varname="trec2019", reference=Trec2019Test)
    RUN = reference(varname="run", reference=Trec2019TestRun)

    @classmethod
    def __create_dataset__(cls, dataset):
        trec2019 = cls.TREC2019.prepare()
        return cls.C(**trec2019.__arguments__(), run=cls.RUN.prepare())


# ---
# --- TREC 2020
# ---


@lua
@dataset(size="12K")
class Trec2020TestQueries(Topics):
    """TREC Deep Learning 2019 (topics)

    Topics of the TREC 2019 MS-Marco Deep Learning track"""

    QUERIES = FileDownloader(
        "queries.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-test2020-queries.tsv.gz",
        checker=HashCheck("00a406fb0d14ed3752d70d1e4eb98600", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.QUERIES.path)


@lua
@datatasks("information retrieval", "passage retrieval")
@datatags("reranking")
@dataset(
    url="https://microsoft.github.io/msmarco/TREC-Deep-Learning-2020.html",
)
class Trec2020TestRun(AdhocRunWithText):
    """TREC Deep Learning (2020)

    Set of query/passages for the passage re-ranking task re-rank (TREC 2020)"""

    RUN = FileDownloader(
        "run.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-passagetest2020-top1000.tsv.gz",
        checker=HashCheck("aa6fbc51d66bd1dc745964c0e140a727", md5),
    )

    @classmethod
    def __create_dataset__(cls, dataset):
        return cls.C(path=cls.RUN.path / "top1000.eval.tsv")
