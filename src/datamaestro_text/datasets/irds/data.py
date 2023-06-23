import ir_datasets
from ir_datasets.formats import GenericDoc, GenericQuery, GenericDocPair
import logging
import attrs
from experimaestro import Config
from experimaestro.compat import cached_property
from typing import Any, Iterator, Tuple
from experimaestro import Option
import datamaestro_text.data.ir as ir
from datamaestro_text.data.ir.data import (
    Topic,
    Document,
    GenericDocument,
    GenericTopic,
    AdhocAssessedTopic,
    SimpleAdhocAssessment,
    IDDocument,
    IDTopic,
)


# Interface between ir_datasets and datamaestro:
# provides adapted data types


class IRDSId(Config):
    irds: Option[str]
    """The id to load the dataset from ir_datasets"""

    @classmethod
    def __xpmid__(cls):
        return f"ir_datasets.{cls.__qualname__}"

    @cached_property
    def dataset(self):
        return ir_datasets.load(self.irds)

    def iter(self) -> Iterator[ir.Topic]:
        """Returns an iterator over topics"""
        for query in self.dataset.queries_iter():
            yield self.factory(query)

    def count(self):
        return self.dataset.queries_count()


class AdhocAssessments(ir.AdhocAssessments, IRDSId):
    def iter(self):
        """Returns an iterator over assessments"""
        ds = self.dataset

        class Qrels(dict):
            def __missing__(self, key):
                qqrel = AdhocAssessedTopic(key, [])
                self[key] = qqrel
                return qqrel

        qrels = Qrels()
        for qrel in ds.qrels_iter():
            qrels[qrel.query_id].assessments.append(
                SimpleAdhocAssessment(qrel.doc_id, qrel.relevance)
            )

        return qrels.values()


def tuple_constructor(cls):
    def constructor(entry):
        return cls(*tuple(entry))

    return constructor


@attrs.define()
class IRDSDocumentWrapper(ir.Document):
    doc: Any


class Documents(ir.DocumentStore, IRDSId):
    CONVERTERS = {GenericDoc: (GenericDocument, tuple_constructor)}

    """Wraps an ir datasets collection -- and provide a default text
    value depending on the collection itself"""

    # List of fields
    # self.dataset.docs_cls()._fields

    def iter(self) -> Iterator[ir.Document]:
        """Returns an iterator over adhoc documents"""
        for doc in self.dataset.docs_iter():
            yield self.converter(doc)

    @property
    def documentcount(self):
        return self.dataset.docs_count()

    @cached_property
    def converter(self):
        return Documents.CONVERTERS.get(
            self.dataset.docs_cls(), lambda doc: IRDSDocumentWrapper(doc)
        )

    @cached_property
    def store(self):
        return self.dataset.docs_store()

    def docid_internal2external(self, ix: int):
        return self.dataset.docs_iter()[ix].doc_id

    def document_ext(self, docid: str) -> Document:
        return self.converter(self.store.get(docid))

    def document_int(self, ix):
        return self.converter(self.dataset.docs_iter()[ix])

    @cached_property
    def document_cls(self):
        return Documents.CONVERTERS[self.dataset.docs_cls()][0]

    @cached_property
    def converter(self):
        document_cls, constructor = Documents.CONVERTERS[self.dataset.docs_cls()]
        return constructor(document_cls)


@attrs.define()
class IRDSQueryWrapper(ir.Topic):
    query: Any


class Topics(ir.TopicsStore, IRDSId):
    CONVERTERS = {GenericQuery: (GenericTopic, tuple_constructor)}

    def iter(self) -> Iterator[ir.Topic]:
        """Returns an iterator over topics"""
        for query in self.dataset.queries_iter():
            yield self.converter(query)

    def count(self):
        return self.dataset.queries_count()

    def topic_int(self, internal_topic_id: int) -> Topic:
        """Returns a document given its internal ID"""
        return self.topics_list[internal_topic_id]

    def topic_ext(self, external_topic_id: int) -> Topic:
        """Returns a document given its external ID"""
        return self.topics_map[external_topic_id]

    @cached_property
    def topics_map(self):
        return self.topics[0]

    @cached_property
    def topics_list(self):
        return self.topics[1]

    @cached_property
    def topics(self):
        topic_map = {}
        topic_list = []
        for query in self.iter():
            topic_list.append(query)
            topic_map[query.get_id()] = query

        return topic_map, topic_list

    @cached_property
    def topic_cls(self):
        return Topics.CONVERTERS[self.dataset.queries_cls()][0]

    @cached_property
    def converter(self):
        topic_cls, constructor = Topics.CONVERTERS[self.dataset.queries_cls()]
        return constructor(topic_cls)


class Adhoc(ir.Adhoc, IRDSId):
    pass


class AdhocRun(ir.AdhocRun, IRDSId):
    pass


class TrainingTriplets(ir.TrainingTriplets, IRDSId):
    """Training triplets from IR Dataset"""

    CONVERTERS = {
        GenericDocPair: lambda qid, doc1_id, doc2_id: (
            IDTopic(qid),
            IDDocument(doc1_id),
            IDDocument(doc2_id),
        )
    }

    @cached_property
    def topic_cls(self):
        return IDTopic

    @cached_property
    def document_cls(self):
        return IDDocument

    @cached_property
    def converter(self):
        return TrainingTriplets.CONVERTERS[self.dataset.docpairs_cls()]

    def iter(self) -> Iterator[Tuple[ir.Topic, ir.Document, ir.Document]]:
        ds = self.dataset

        logging.info("Starting to generate triplets")
        yield from (self.converter(*entry) for entry in ds.docpairs_iter())
        logging.info("Ending triplet generation")

    def count(self):
        """Returns the length or None"""
        return self.dataset.docpairs_count()
