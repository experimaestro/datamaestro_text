"""MS Marco Passage Ranking

  MS MARCO(Microsoft Machine Reading Comprehension) is a large scale dataset focused on machine reading comprehension, question answering, and passage ranking. A variant of this task will be the part of TREC and AFIRM 2019. For Updates about TREC 2019 please follow This Repository Passage Reranking task Task Given a query q and a the 1000 most relevant passages P = p1, p2, p3,... p1000, as retrieved by BM25 a succeful system is expected to rerank the most relevant passage as high as possible. For this task not all 1000 relevant items have a human labeled relevant passage. Evaluation will be done using MRR.
"""

from datamaestro.download.single import filedownloader
from datamaestro.download import reference
from datamaestro.definitions import data, argument, datatasks, datatags, dataset
from datamaestro.download.archive import tardownloader
from datamaestro_text.data.ir import RerankAdhoc, Adhoc
from datamaestro_text.data.ir.csv import AdhocTopics, AdhocRunWithText, AdhocDocuments
from datamaestro_text.data.ir.trec import AdhocAssessments

#@filedownloader('queries_trec2019', url='https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-test2019-queries.tsv.gz')
#@filedownloader('msrun_trec2019', url='https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-passagetest2019-top1000.tsv.gz')
#@filedownloader('qidpidtriples_train_full', url='https://msmarco.blob.core.windows.net/msmarcoranking/qidpidtriples.train.full.tar.gz')


@filedownloader('collection', url='https://msmarco.blob.core.windows.net/msmarcoranking/collection.tar.gz')
@dataset(AdhocDocuments)
def collection(AdhocDocuments):
  return { "path": collection / "documents.tsv" }

# --- Train

@tardownloader("run", url="https://msmarco.blob.core.windows.net/msmarcoranking/top1000.train.tar.gz")
@dataset(AdhocTopics) 
def run_train(queries):
  return { "path": queries / "top1000.train.tsv" }


@tardownloader("queries", url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz", files=["queries.train.tsv"])
@dataset(AdhocTopics) 
def queries_train(queries):
  return { "path": queries / "queries.train.tsv" }

@filedownloader('qrels', url='https://msmarco.blob.core.windows.net/msmarcoranking/qrels.train.tsv')
@dataset(AdhocAssessments) 
def qrels_train():
  { "path": qrels }

@reference("collection", collection)
@reference("topics", qrels_train)
@reference("qrels", qrels_train)
@datatasks("information retrieval", "passage retrieval")
@dataset(Adhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def train():
    return {
      "documents": collection,
      "topics": queries_train,
      "assessments": qrels_train,
    }

@reference("train", train)
@reference("run", run_train)
@datatasks("information retrieval", "passage retrieval")
@dataset(RerankAdhoc, url="https://github.com/microsoft/MSMARCO-Passage-Ranking")
def train_withrun(train, run):
  return {
    **train, 
    "run": run
  }

# --- Val

@tardownloader("queries", url="https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz", files=["queries.val.tsv"])
@dataset(AdhocTopics) 
def queries_val(queries):
  return { "path": queries / "queries.val.tsv" }

@filedownloader('qrels_dev', url='https://msmarco.blob.core.windows.net/msmarcoranking/qrels.dev.tsv')
@dataset(AdhocAssessments) 
def qrels_val():
  pass

# --- Test




    
# @filedownloader('queries', url='https://msmarco.blob.core.windows.net/msmarcoranking/queries.tar.gz')

# For re-ranking
# @filedownloader('msrun_dev', url='https://msmarco.blob.core.windows.net/msmarcoranking/top1000.dev.tar.gz')
# @filedownloader('msrun_eval', url='https://msmarco.blob.core.windows.net/msmarcoranking/top1000.eval.tar.gz')
