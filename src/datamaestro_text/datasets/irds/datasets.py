from contextlib import contextmanager
import os
from typing import Iterable
from ir_datasets import registry, corpus_id, load

from datamaestro.definitions import AbstractDataset
from .data import (
    AdhocAssessments,
    AdhocRun,
    Documents,
    Topics,
    Adhoc,
    IRDSId,
    TrainingTriplets,
)


class Dataset(AbstractDataset):
    SUFFIX = ""
    __configtype__ = None

    def __init__(self, repository, irds_id, irds_ds):
        super().__init__(repository)
        self.id = (
            f"""irds.{irds_id.replace("/", ".")}"""
            f"""{"." + self.SUFFIX if self.SUFFIX else ""}"""
        )
        self.irds_id = irds_id
        self.irds_ds = irds_ds

    @property
    def fullid(self):
        return f"{self.id}@{self.repository.name}"

    @property
    def description(self):
        return self.irds_ds.documentation()["desc"]

    def hasfiles(self):
        return False

    def download(self, force=False):
        return True

    def prepare(self, download=True):
        ds: IRDSId = super().prepare(download=download)
        ds.irds = self.irds_id
        if download:
            self.download()

        return ds

    @property
    def configtype(self):
        return self.__class__.__configtype__


class QrelsDataset(Dataset):
    SUFFIX = "qrels"
    configtype = AdhocAssessments

    def download(self, force=False):
        # Triggers download
        next(self.irds_ds.qrels_iter())
        return True

    def _prepare(self, download=False) -> Documents:
        return AdhocAssessments(id=self.fullid)


class QueriesDataset(Dataset):
    SUFFIX = "queries"
    configtype = Topics

    def download(self, force=False):
        # Triggers download
        next(self.irds_ds.queries_iter())
        return True

    def _prepare(self, download=False) -> Documents:
        return Topics(id=self.fullid)


# class ScoredDocuments(Dataset):
#     SUFFIX = "scored-documents"
#     base = ScoredDocuments


class DocumentsDataset(Dataset):
    SUFFIX = "documents"
    configtype = Documents

    def download(self, force=False):
        # Triggers download
        next(self.irds_ds.docs_iter())
        return True

    def _prepare(self, download=False) -> Documents:
        return Documents(id=self.fullid)


class TrainingTripletsDataset(Dataset):
    SUFFIX = "docpairs"

    def _prepare(self, download=False) -> Documents:
        return TrainingTriplets(
            id=self.fullid,
        )


class AdhocRunDataset(Dataset):
    SUFFIX = "scoreddocs"
    base = AdhocRun
    configtype = AdhocRun

    def _prepare(self, download=False) -> Documents:
        return AdhocRun(id=self.fullid)


class Collection(Dataset):
    base = Adhoc
    assessements: QrelsDataset
    topics: QueriesDataset

    def _prepare(self, download=False) -> Documents:
        return Adhoc(
            id=self.fullid,
            topics=self.topics.prepare(download),
            assessments=self.assessments.prepare(download),
            documents=self.documents.prepare(download),
        )


class Datasets:
    """Simple wrapper holding related data pieces"""

    def __init__(self, key, title, description):
        self.id = key
        self.title = title
        self.description = description
        self.datasets = []

    def __iter__(self) -> Iterable[AbstractDataset]:
        return self.datasets.__iter__()


IRDS_NO_WARNING_KEY = "IR_DATASETS_SKIP_DEPRECATED_WARNING"


@contextmanager
def no_deprecated_warnings():
    """Context manager to remove ir dataset warnings"""
    old = os.environ.get(IRDS_NO_WARNING_KEY, "")
    os.environ[IRDS_NO_WARNING_KEY] = "true"
    yield None
    os.environ[IRDS_NO_WARNING_KEY] = old


def build(repository):
    """Builds a datamaestro repository by using ir_datasets registry"""
    datasets = {}
    bykey = {}

    def add(cid, ds):
        datasets[cid].datasets.append(ds)
        bykey[ds.id] = ds

    with no_deprecated_warnings():
        for dataset_id in registry:
            ds = load(dataset_id)

            # Skip deprecated datasets
            if hasattr(ds, "deprecated"):
                continue

            if not ds.has_docs():
                # Abstract dataset
                continue

            cid = corpus_id(dataset_id)
            queries = None
            qrels = None

            if cid == dataset_id:
                # If the corpus ID is the current dataset ID
                module = Datasets(
                    cid,
                    ds.documentation().get("pretty_name", cid),
                    ds.documentation()["desc"],
                )
                datasets[cid] = module
                add(cid, DocumentsDataset(repository, dataset_id, ds))

            if ds.has_queries():
                queries = QueriesDataset(repository, dataset_id, ds)
                add(cid, queries)

            if ds.has_docpairs():
                add(cid, TrainingTripletsDataset(repository, dataset_id, ds))

            if ds.has_scoreddocs():
                add(cid, AdhocRunDataset(repository, dataset_id, ds))

            if ds.has_qrels():
                qrels = QrelsDataset(repository, dataset_id, ds)
                add(cid, qrels)

            if qrels and queries:
                collection = Collection(repository, dataset_id, ds)
                collection.documents = datasets[cid].datasets[0]
                collection.topics = queries
                collection.assessments = qrels

                add(cid, collection)

        return list(datasets.values()), bykey
