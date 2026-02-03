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
from datamaestro.definitions import Dataset, datatasks, datatags, dataset
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
class CollectionEtc(Dataset):
    """Documents and some more files"""

    DATA = TarDownloader(
        "data",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/collectionandqueries.tar.gz",
        checker=HashCheck("31644046b18952c1386cd4564ba2ae69", md5),
    )

    def config(self) -> Folder:
        return Folder.C(path=self.DATA.path)


@lua
@dataset(size="2.9GB")
class Collection(Dataset):
    """MS-Marco documents

    This file contains each passage in the larger MSMARCO dataset.

    Format is TSV (PID \\t Passage)"""

    DATA = reference(varname="data", reference=CollectionEtc)

    def config(self) -> Documents:
        return Documents.C(path=self.DATA.prepare().path / "collection.tsv")


# --- Train


@lua
@dataset(size="2.5GB")
class TrainRun(Dataset):
    """

    TSV format: qid, pid, query, passage
    """

    RUN = TarDownloader(
        "run",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.train.tar.gz",
        checker=HashCheck("d99fdbd5b2ea84af8aa23194a3263052", md5),
    )

    def config(self) -> AdhocRunWithText:
        return AdhocRunWithText.C(path=self.RUN.path / "top1000.train.tsv")


@lua
@dataset()
class TrainQueries(Dataset):
    QUERIES = TarDownloader(
        "queries",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz",
        files=["queries.train.tsv"],
        checker=HashCheck("c177b2795d5f2dcc524cf00fcd973be1", md5),
    )

    def config(self) -> Topics:
        return Topics.C(path=self.QUERIES.path / "queries.train.tsv")


@lua
@dataset(size="10.1MB")
class TrainQrels(Dataset):
    QRELS = FileDownloader(
        "qrels.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/qrels.train.tsv",
        checker=HashCheck("733fb9fe12d93e497f7289409316eccf", md5),
    )

    def config(self) -> TrecAdhocAssessments:
        return TrecAdhocAssessments.C(path=self.QRELS.path)


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class Train(Dataset):
    """MS-Marco train dataset"""

    COLLECTION = reference(varname="collection", reference=Collection)
    TOPICS = reference(varname="topics", reference=TrainQueries)
    QRELS = reference(varname="qrels", reference=TrainQrels)

    def config(self) -> Adhoc:
        return Adhoc.C(
            documents=self.COLLECTION.prepare(),
            topics=self.TOPICS.prepare(),
            assessments=self.QRELS.prepare(),
        )


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class TrainWithrun(Dataset):
    """MSMarco train dataset, including the top-1000 to documents to re-rank"""

    TRAIN = reference(varname="train", reference=Train)
    RUN = reference(varname="run", reference=TrainRun)

    def config(self) -> RerankAdhoc:
        train = self.TRAIN.prepare()
        return RerankAdhoc.C(**train.__arguments__(), run=self.RUN.prepare())


# Training triplets


@dataset(
    url="https://github.com/microsoft/MSMARCO-Passage-Ranking",
    size="5.7GB",
)
class TrainIdtriples(Dataset):
    """Full training triples (query, positive passage, negative passage) with IDs"""

    TRIPLES = FileDownloader(
        "triples.tsv",
        size=1_841_693_309,
        url="https://msmarco.blob.core.windows.net/msmarcoranking/qidpidtriples.train.full.2.tsv.gz",
        checker=HashCheck("4e58f45f82f3fe99e3239ecffd8ed371", md5),
    )

    def config(self) -> TrainingTripletsLines:
        return TrainingTripletsLines.C(
            path=self.TRIPLES.path, doc_ids=True, topic_ids=True
        )


@dataset(
    url="https://github.com/microsoft/MSMARCO-Passage-Ranking",
    size="27.1GB",
)
class TrainTexttriplesSmall(Dataset):
    """Small training triples (query, positive passage, negative passage) with text"""

    TRIPLES = FileDownloader(
        "triples.tsv",
        size=7_930_881_353,
        url="https://msmarco.blob.core.windows.net/msmarcoranking/triples.train.small.tar.gz",
        checker=HashCheck("c13bf99ff23ca691105ad12eab837f84", md5),
    )

    def config(self) -> TrainingTripletsLines:
        return TrainingTripletsLines.C(path=self.TRIPLES.path)


@dataset(
    url="https://github.com/microsoft/MSMARCO-Passage-Ranking",
    size="272.2GB",
)
class TrainTexttripleFull(Dataset):
    """Full training triples (query, positive passage, negative passage) with text"""

    TRIPLES = FileDownloader(
        "triples.tsv",
        size=77_877_731_328,
        url="https://msmarco.blob.core.windows.net/msmarcoranking/triples.train.full.tar.gz",
        checker=HashCheck("8d509d484ea1971e792b812ae4800c6f", md5),
    )

    def config(self) -> TrainingTripletsLines:
        return TrainingTripletsLines.C(path=self.TRIPLES.path)


# ---
# --- Development set
# ---


@lua
@dataset()
class DevQueries(Dataset):
    QUERIES = TarDownloader(
        "queries",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz",
        files=["queries.dev.tsv"],
        checker=HashCheck("c177b2795d5f2dcc524cf00fcd973be1", md5),
    )

    def config(self) -> Topics:
        return Topics.C(path=self.QUERIES.path / "queries.dev.tsv")


@lua
@dataset()
class DevRun(Dataset):
    RUN = TarDownloader(
        "run",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.dev.tar.gz",
        checker=HashCheck("8c140662bdf123a98fbfe3bb174c5831", md5),
    )

    def config(self) -> AdhocRunWithText:
        return AdhocRunWithText.C(path=self.RUN.path / "top1000.eval.tsv")


@lua
@dataset()
class DevQrels(Dataset):
    QRELS = FileDownloader(
        "qrels.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/qrels.dev.tsv",
        checker=HashCheck("9157ccaeaa8227f91722ba5770787b16", md5),
    )

    def config(self) -> TrecAdhocAssessments:
        return TrecAdhocAssessments.C(path=self.QRELS.path)


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class Dev(Dataset):
    """MS-Marco dev dataset"""

    COLLECTION = reference(varname="collection", reference=Collection)
    TOPICS = reference(varname="topics", reference=DevQueries)
    QRELS = reference(varname="qrels", reference=DevQrels)

    def config(self) -> Adhoc:
        return Adhoc.C(
            documents=self.COLLECTION.prepare(),
            topics=self.TOPICS.prepare(),
            assessments=self.QRELS.prepare(),
        )


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class DevWithrun(Dataset):
    """MSMarco dev dataset, including the top-1000 to documents to re-rank"""

    DEV = reference(varname="dev", reference=Dev)
    RUN = reference(varname="run", reference=DevRun)

    def config(self) -> RerankAdhoc:
        dev = self.DEV.prepare()
        return RerankAdhoc.C(**dev.__arguments__(), run=self.RUN.prepare())


@lua
@dataset()
class EvalWithrun(Dataset):
    RUN = TarDownloader(
        "run",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.eval.tar.gz",
        checker=HashCheck("73778cd99f6e0632d12d0b5731b20a02", md5),
    )

    def config(self) -> AdhocRunWithText:
        return AdhocRunWithText.C(path=self.RUN.path / "top1000.eval.tsv")


# ---
# --- Relevant Passages
# --- https://github.com/microsoft/MSMARCO-Passage-Ranking#relevant-passages
# ---


@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class DevSmallQueries(Dataset):
    DATA = reference(varname="data", reference=CollectionEtc)

    def config(self) -> Topics:
        return Topics.C(path=self.DATA.prepare().path / "queries.dev.small.tsv")


@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class DevSmallQrels(Dataset):
    DATA = reference(varname="data", reference=CollectionEtc)

    def config(self) -> TrecAdhocAssessments:
        return TrecAdhocAssessments.C(
            path=self.DATA.prepare().path / "qrels.dev.small.tsv"
        )


@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class DevSmall(Dataset):
    TOPICS = reference(varname="topics", reference=DevSmallQueries)
    QRELS = reference(varname="qrels", reference=DevSmallQrels)
    COLLECTION = reference(varname="collection", reference=Collection)

    def config(self) -> Adhoc:
        return Adhoc.C(
            documents=self.COLLECTION.prepare(),
            topics=self.TOPICS.prepare(),
            assessments=self.QRELS.prepare(),
        )


@dataset(url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
class EvalQueriesSmall(Dataset):
    DATA = reference(varname="data", reference=CollectionEtc)

    def config(self) -> Topics:
        return Topics.C(path=self.DATA.prepare().path / "queries.eval.small.tsv")


# ---
# --- TREC 2019
# ---


@lua
@dataset()
class Trec2019TestQueries(Dataset):
    QUERIES = FileDownloader(
        "queries.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-test2019-queries.tsv.gz",
        checker=HashCheck("756e60d714cee28d3b552289d6272f1d", md5),
    )

    def config(self) -> Topics:
        return Topics.C(path=self.QUERIES.path)


@lua
@dataset()
class Trec2019TestRun(Dataset):
    RUN = FileDownloader(
        "run.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-passagetest2019-top1000.tsv.gz",
        checker=HashCheck("ec9e012746aa9763c7ff10b3336a3ce1", md5),
    )

    def config(self) -> AdhocRunWithText:
        return AdhocRunWithText.C(path=self.RUN.path / "top1000.eval.tsv")


@lua
@dataset()
class Trec2019TestQrels(Dataset):
    QRELS = FileDownloader(
        "qrels.tsv",
        url="https://trec.nist.gov/data/deep/2019qrels-pass.txt",
        checker=HashCheck("2f4be390198da108f6845c822e5ada14", md5),
    )

    def config(self) -> TrecAdhocAssessments:
        return TrecAdhocAssessments.C(path=self.QRELS.path)


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://microsoft.github.io/msmarco/TREC-Deep-Learning-2019.html")
class Trec2019Test(Dataset):
    "TREC Deep Learning (2019)"

    COLLECTION = reference(varname="collection", reference=Collection)
    TOPICS = reference(varname="topics", reference=Trec2019TestQueries)
    QRELS = reference(varname="qrels", reference=Trec2019TestQrels)

    def config(self) -> Adhoc:
        return Adhoc.C(
            documents=self.COLLECTION.prepare(),
            topics=self.TOPICS.prepare(),
            assessments=self.QRELS.prepare(),
        )


@lua
@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://microsoft.github.io/msmarco/TREC-Deep-Learning-2019.html")
class Trec2019TestWithrun(Dataset):
    """TREC Deep Learning (2019), including the top-1000 to documents to re-rank"""

    TREC2019 = reference(varname="trec2019", reference=Trec2019Test)
    RUN = reference(varname="run", reference=Trec2019TestRun)

    def config(self) -> RerankAdhoc:
        trec2019 = self.TREC2019.prepare()
        return RerankAdhoc.C(**trec2019.__arguments__(), run=self.RUN.prepare())


# ---
# --- TREC 2020
# ---


@lua
@dataset(size="12K")
class Trec2020TestQueries(Dataset):
    """TREC Deep Learning 2019 (topics)

    Topics of the TREC 2019 MS-Marco Deep Learning track"""

    QUERIES = FileDownloader(
        "queries.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-test2020-queries.tsv.gz",
        checker=HashCheck("00a406fb0d14ed3752d70d1e4eb98600", md5),
    )

    def config(self) -> Topics:
        return Topics.C(path=self.QUERIES.path)


@lua
@datatasks("information retrieval", "passage retrieval")
@datatags("reranking")
@dataset(
    url="https://microsoft.github.io/msmarco/TREC-Deep-Learning-2020.html",
)
class Trec2020TestRun(Dataset):
    """TREC Deep Learning (2020)

    Set of query/passages for the passage re-ranking task re-rank (TREC 2020)"""

    RUN = FileDownloader(
        "run.tsv",
        url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-passagetest2020-top1000.tsv.gz",
        checker=HashCheck("aa6fbc51d66bd1dc745964c0e140a727", md5),
    )

    def config(self) -> AdhocRunWithText:
        return AdhocRunWithText.C(path=self.RUN.path / "top1000.eval.tsv")
