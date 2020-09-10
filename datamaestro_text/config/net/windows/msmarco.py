"""MS Marco Passage Ranking

  MS MARCO(Microsoft Machine Reading Comprehension) is a large scale dataset focused on machine reading comprehension, question answering, and passage ranking. A variant of this task will be the part of TREC and AFIRM 2019. For Updates about TREC 2019 please follow This Repository Passage Reranking task Task Given a query q and a the 1000 most relevant passages P = p1, p2, p3,... p1000, as retrieved by BM25 a succeful system is expected to rerank the most relevant passage as high as possible. For this task not all 1000 relevant items have a human labeled relevant passage. Evaluation will be done using MRR.

  Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, RanganMajumder, and Li Deng. 2016.
  MS MARCO: A Human Generated MAchineReading COmprehension Dataset. In CoCo@NIPS.


  See https://github.com/microsoft/MSMARCO-Passage-Ranking for more details
"""

from datamaestro.annotations.agreement import useragreement
from datamaestro.download.single import filedownloader
from datamaestro.download import reference
from datamaestro.definitions import data, argument, datatasks, datatags, dataset
from datamaestro.download.archive import tardownloader
from datamaestro_text.data.ir import RerankAdhoc, Adhoc, AdhocRun
from datamaestro_text.data.ir.csv import AdhocTopics, AdhocRunWithText, AdhocDocuments
from datamaestro_text.data.ir.trec import TrecAdhocAssessments
from datamaestro.utils import HashCheck
from hashlib import md5


lua = useragreement(
    """Will begin downloading MS-MARCO dataset.
Please confirm you agree to the authors' data usage stipulations found at
http://www.msmarco.org/dataset.aspx""",
    id="net.windows.msmarco",
)

# --- Document collections


@lua
@tardownloader(
    "collection",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/collection.tar.gz",
    checker=HashCheck("87dd01826da3e2ad45447ba5af577628", md5),
)
@dataset(AdhocDocuments, size="2.9GB")
def collection(collection):
    """This file contains each unique Passage in the larger MSMARCO dataset. Format is PID\tPassage."""
    return {"path": collection / "collection.tsv"}


# --- Train


@lua
@tardownloader(
    "run",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.train.tar.gz",
    checker=HashCheck("d99fdbd5b2ea84af8aa23194a3263052", md5),
)
@dataset(AdhocRunWithText)
def train_run(run):
    return {"path": run / "top1000.train.tsv"}


@lua
@tardownloader(
    "queries",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz",
    files=["queries.train.tsv"],
    checker=HashCheck("c177b2795d5f2dcc524cf00fcd973be1", md5),
)
@dataset(AdhocTopics)
def train_queries(queries):
    return {"path": queries / "queries.train.tsv"}


@lua
@filedownloader(
    "qrels.tsv",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/qrels.train.tsv",
    checker=HashCheck("733fb9fe12d93e497f7289409316eccf", md5),
)
@dataset(TrecAdhocAssessments, size="10.1MB")
def train_qrels(qrels):
    return {"path": qrels}


@lua
@reference("collection", collection)
@reference("topics", train_queries)
@reference("qrels", train_qrels)
@datatasks("information retrieval", "passage retrieval")
@dataset(Adhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def train(topics, qrels, collection):
    return {
        "documents": collection,
        "topics": topics,
        "assessments": qrels,
    }


@lua
@reference("train", train)
@reference("run", train_run)
@datatasks("information retrieval", "passage retrieval")
@dataset(RerankAdhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def train_withrun(train, run):
    """MSMarco train dataset, including the top-1000 to documents to re-rank"""
    return {**train.__arguments__(), "run": run}


# --- Development


@lua
@tardownloader(
    "queries",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz",
    files=["queries.dev.tsv"],
    checker=HashCheck("c177b2795d5f2dcc524cf00fcd973be1", md5),
)
@dataset(AdhocTopics)
def dev_queries(queries):
    return {"path": queries / "queries.val.tsv"}


@lua
@tardownloader(
    "run",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.dev.tar.gz",
    checker=HashCheck("8c140662bdf123a98fbfe3bb174c5831", md5),
)
@dataset(AdhocRunWithText)
def dev_run(run):
    return {"path": run / "top1000.eval.tsv"}


@lua
@filedownloader(
    "qrels.tsv",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/qrels.dev.tsv",
    checker=HashCheck("9157ccaeaa8227f91722ba5770787b16", md5),
)
@dataset(TrecAdhocAssessments)
def dev_qrels(qrels):
    return {"path": qrels}


@lua
@reference("collection", collection)
@reference("topics", dev_queries)
@reference("qrels", dev_qrels)
@datatasks("information retrieval", "passage retrieval")
@dataset(Adhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def dev(topics, qrels, collection):
    return {
        "documents": collection,
        "topics": topics,
        "assessments": qrels,
    }


@lua
@reference("dev", dev)
@reference("run", dev_run)
@datatasks("information retrieval", "passage retrieval")
@dataset(RerankAdhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def dev_withrun(dev, run):
    """MSMarco dev dataset, including the top-1000 to documents to re-rank"""
    return {**dev.__arguments__(), "run": run}


# --- Test (eval): there is no (as for now) test assessments


@lua
@tardownloader(
    "queries",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz",
    files=["queries.eval.tsv"],
    checker=HashCheck("c177b2795d5f2dcc524cf00fcd973be1", md5),
)
@dataset(AdhocTopics)
def eval_queries(queries):
    return {"path": queries / "queries.val.tsv"}


@lua
@tardownloader(
    "run",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.eval.tar.gz",
    checker=HashCheck("73778cd99f6e0632d12d0b5731b20a02", md5),
)
@dataset(AdhocRunWithText)
def eval_withrun(run):
    return {"path": run / "top1000.eval.tsv"}


# --- TREC 2019


@lua
@filedownloader(
    "queries.tsv",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-test2019-queries.tsv.gz",
    checker=HashCheck("756e60d714cee28d3b552289d6272f1d", md5),
)
@dataset(AdhocTopics)
def trec2019_test_queries(queries):
    return {"path": queries}


@lua
@filedownloader(
    "run.tsv",
    url="https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-passagetest2019-top1000.tsv.gz",
    checker=HashCheck("ec9e012746aa9763c7ff10b3336a3ce1", md5),
)
@dataset(AdhocRunWithText)
def trec2019_test_run(run):
    return {"path": run / "top1000.eval.tsv"}


@lua
@filedownloader(
    "qrels.tsv",
    url="https://trec.nist.gov/data/deep/2019qrels-pass.txt",
    checker=HashCheck("2f4be390198da108f6845c822e5ada14", md5),
)
@dataset(TrecAdhocAssessments)
def trec2019_test_qrels(qrels):
    return {"path": qrels}


@lua
@reference("collection", collection)
@reference("topics", trec2019_test_queries)
@reference("qrels", trec2019_test_qrels)
@datatasks("information retrieval", "passage retrieval")
@dataset(Adhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def trec2019_test(topics, qrels, collection):
    return {
        "documents": collection,
        "topics": topics,
        "assessments": qrels,
    }


@lua
@reference("trec2019", trec2019_test)
@reference("run", trec2019_test_run)
@datatasks("information retrieval", "passage retrieval")
@dataset(RerankAdhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def trec2019_test_withrun(trec2019, run):
    """MSMarco dev dataset, including the top-1000 to documents to re-rank"""
    return {**trec2019.__arguments__(), "run": run}
