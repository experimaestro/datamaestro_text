import logging
import gzip
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type
from experimaestro import Config, Task, Param, Annotated, pathgenerator, Option, tqdm
import numpy as np
import datamaestro_text.data.ir as ir
from datamaestro_text.utils.shuffle import shuffle


def getpathname(context, config):
    name = "triplets.lst"
    if config.compressed:
        name = "triplets.lst.gz"

    return context.currentpath() / name


class StoreTrainingTripletTopicAdapter(ir.TrainingTriplets):
    """Retrieve an adhoc topic text from a topic store (given the topic ID)"""

    id: Param[str] = ""

    store: Param[ir.TopicsStore]
    """The topic store to use"""

    data: Param[ir.TrainingTriplets]
    """Input data"""

    def __validate__(self):
        assert self.data.topic_cls.has_id, "Topics have no ID"

    def iter(self):
        for topic, doc1, doc2 in self.data.iter():
            yield self.store.topic_ext(topic.get_id()), doc1, doc2

    def count(self):
        return self.data.count()

    @property
    def topic_cls(self) -> Type[ir.Topic]:
        """The class for topics"""
        return self.store.topic_cls

    @property
    def document_cls(self) -> Type[ir.Document]:
        """The class for documents"""
        return self.data.document_cls


class StoreTrainingTripletDocumentAdapter(ir.TrainingTriplets):
    """Transforms training triplets to add the document text from a document store"""

    id: Param[str] = ""

    store: Param[ir.DocumentStore]
    """The topic store to use"""

    data: Param[ir.TrainingTriplets]
    """Input data"""

    def __validate__(self):
        assert self.data.document_cls.has_id, "Documents have no ID"

    def iter(self):
        for topic, doc1, doc2 in self.data.iter():
            yield topic, self.store.document_ext(
                doc1.get_id()
            ), self.store.document_ext(doc2.get_id())

    def count(self):
        return self.data.count()

    @property
    def topic_cls(self) -> Type[ir.Topic]:
        """The class for topics"""
        return self.store.topic_cls

    @property
    def document_cls(self) -> Type[ir.Document]:
        """The class for documents"""
        return self.data.document_cls


class ShuffledTrainingTripletsLines(Task):
    """Shuffle a set of training triplets"""

    data: Param[ir.TrainingTriplets]
    """Input data"""

    path: Annotated[Path, pathgenerator(getpathname)]
    """Output path"""

    doc_ids: Param[bool]
    """Whether to use document ids"""

    topic_ids: Param[bool]
    """True if we have query IDs"""

    seed: Param[int]
    """The random seed"""

    compressed: Option[bool] = True
    """Compress the output"""

    sample_rate: Param[float] = 1.0
    """Sampling rate - set to 1 to keep all the samples"""

    sample_max: Param[int] = 0
    """Maximum number of samples"""

    tmp_path: Annotated[Path, pathgenerator("tmp")]
    """Path where temporary files will be stored"""

    def __validate__(self):
        if self.topic_ids:
            assert self.data.topic_cls.has_id, "No topic ID in the source data"
        else:
            assert self.data.topic_cls.has_text, "No topic text in the source data"

        if self.doc_ids:
            assert self.data.document_cls.has_id, "No doc ID in the source data"
        else:
            assert self.data.document_cls.has_text, "No doc text in the source data"

    def task_outputs(self, dep):
        return dep(
            ir.TrainingTripletsLines(
                id="",
                path=self.path,
                topic_ids=self.topic_ids,
                doc_ids=self.doc_ids,
                sep="\t",
            )
        )

    def execute(self):
        # --- Shuffle using the shuf command with a seed

        random = np.random.RandomState(self.seed)

        if self.topic_ids:

            def get_query(query):
                return query.get_id()

        else:

            def get_query(query):
                return query.get_text()

        if self.doc_ids:

            def get_doc(doc):
                return doc.get_id()

        else:

            def get_doc(doc):
                return doc.get_text()

        def triplegenerator():
            logging.info("Starting to output triples")
            count = 0

            total = self.data.count()
            if self.sample_max > 0:
                total = min(total, self.sample_max)

            pbar = tqdm(total=total)
            for query, doca, docb in self.data.iter():
                # Discard sample
                if self.sample_rate < 1:
                    if random.uniform() > self.sample_rate:
                        continue

                pbar.update(1)
                count += 1
                yield f"{get_query(query)}\t{get_doc(doca)}\t{get_doc(docb)}\n"

                if self.sample_max > 0 and count >= self.sample_max:
                    break

            logging.info("Triples output ended (%d triples)", count)

        logging.info("Creating generator")

        # Output can be a stream or nothing
        if self.compressed:
            output = gzip.open(self.path, "wt")
        else:
            output = self.path.open("wt")

        with output:
            self.tmp_path.mkdir(exist_ok=True)
            shuffle(triplegenerator(), output, random=random, tmp_path=self.tmp_path)


class TopicWrapper(Config, ABC):
    """Modify topics on the fly using a topic wrapper"""

    @abstractmethod
    def __call__(topic: ir.Topic) -> ir.Topic:
        """Transforms a topic into another topic"""
        ...
