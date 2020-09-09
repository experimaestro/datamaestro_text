"""MS Marco Passage Ranking

  MS MARCO(Microsoft Machine Reading Comprehension) is a large scale dataset focused on machine reading comprehension, question answering, and passage ranking. A variant of this task will be the part of TREC and AFIRM 2019. For Updates about TREC 2019 please follow This Repository Passage Reranking task Task Given a query q and a the 1000 most relevant passages P = p1, p2, p3,... p1000, as retrieved by BM25 a succeful system is expected to rerank the most relevant passage as high as possible. For this task not all 1000 relevant items have a human labeled relevant passage. Evaluation will be done using MRR.

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

#@filedownloader('queries_trec2019', url='https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-test2019-queries.tsv.gz')
#@filedownloader('msrun_trec2019', url='https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-passagetest2019-top1000.tsv.gz')
#@filedownloader('qidpidtriples_train_full', url='https://msmarco.blob.core.windows.net/msmarcoranking/qidpidtriples.train.full.tar.gz')


lua = useragreement(
    """Will begin downloading MS-MARCO dataset.
Please confirm you agree to the authors' data usage stipulations found at
http://www.msmarco.org/dataset.aspx""", id="net.windows.msmarco"
)

# --- Document collections

@lua
@tardownloader('collection', url='https://msmarco.blob.core.windows.net/msmarcoranking/collection.tar.gz')
@dataset(AdhocDocuments, size="2.9GB")
def collection(collection):
  """This file contains each unique Passage in the larger MSMARCO dataset. Format is PID\tPassage."""
  return { "path": collection / "collection.tsv" }

# --- Train

@lua
@tardownloader("run", url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.train.tar.gz")
@dataset(AdhocRun) 
def run_train(queries):
  return { "path": queries / "top1000.train.tsv" }


@lua
@tardownloader("queries", url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz", files=["queries.train.tsv"])
@dataset(AdhocTopics) 
def queries_train(queries):
  return { "path": queries / "queries.train.tsv" }

@lua
@filedownloader('qrels.tsv', url='https://msmarco.blob.core.windows.net/msmarcoranking/qrels.train.tsv')
@dataset(TrecAdhocAssessments, size="10.1MB") 
def qrels_train(qrels):
  return { "path": qrels }

@lua
@reference("collection", collection)
@reference("topics", queries_train)
@reference("qrels", qrels_train)
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
@reference("run", run_train)
@datatasks("information retrieval", "passage retrieval")
@dataset(RerankAdhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def train_withrun(train, run):
  """MSMarco train dataset, including the top-1000 to documents to re-rank"""
  return {
    **train, 
    "run": run
  }
``
# --- Development

@lua
@tardownloader("queries", url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz", files=["queries.dev.tsv"])
@dataset(AdhocTopics) 
def queries_dev(queries):
  return { "path": queries / "queries.val.tsv" }

@lua
@tardownloader("run", url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.dev.tar.gz")
@dataset(AdhocRun) 
def run_dev(run):
  return { "path": queries / "top1000.eval.tsv" }

@lua
@filedownloader('qrels.tsv', url='https://msmarco.blob.core.windows.net/msmarcoranking/qrels.dev.tsv')
@dataset(TrecAdhocAssessments) 
def qrels_dev(qrels):
  return { "path": qrels }

@lua
@reference("collection", collection)
@reference("topics", queries_dev)
@reference("qrels", qrels_dev)
@datatasks("information retrieval", "passage retrieval")
@dataset(Adhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def dev(topics, qrels, collection):
    return {
      "documents": collection,
      "topics": topics,
      "assessments": qrels,
    }

@lua
@reference("train", dev)
@reference("run", run_dev)
@datatasks("information retrieval", "passage retrieval")
@dataset(RerankAdhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def dev_withrun(dev, run):
  """MSMarco dev dataset, including the top-1000 to documents to re-rank"""
  return {
    **dev, 
    "run": run
  }

# --- Test (eval): there is no (as for now) test assessments

@lua
@tardownloader("queries", url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz", files=["queries.eval.tsv"])
@dataset(AdhocTopics) 
def queries_eval(queries):
  return { "path": queries / "queries.val.tsv" }

@lua
@tardownloader("run", url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.eval.tar.gz")
@dataset(AdhocRun) 
def run_eval(run):
  return { "path": queries / "top1000.eval.tsv" }
