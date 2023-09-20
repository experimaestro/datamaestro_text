import logging
from typing import Any, Iterator, Tuple, Type
import attrs
import ir_datasets
from ir_datasets.formats import (
    GenericDoc,
    GenericQuery,
    GenericDocPair,
    TrecParsedDoc,
    TrecQuery,
)
import ir_datasets.datasets as _irds
from experimaestro import Config
from experimaestro.compat import cached_property
from experimaestro import Option
import datamaestro_text.data.ir as ir
from datamaestro_text.data.ir.base import (
    Topic,
    Document,
    GenericDocument,
    GenericTopic,
    AdhocAssessedTopic,
    SimpleAdhocAssessment,
    IDDocument,
    IDTopic,
)
import datamaestro_text.data.ir.formats as formats


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


class tuple_constructor:
    def __init__(self, target_cls: Type, *fields: str):
        self.target_cls = target_cls
        self.fields = fields

    def check(self, source_cls: Type):
        assert (
            source_cls._fields == self.fields
        ), f"Internal error: Fields do not match ({source_cls._fields} and {self.fields})"

    def __call__(self, entry):
        return self.target_cls(*tuple(entry))


@attrs.define()
class IRDSDocumentWrapper(ir.Document):
    doc: Any


class Documents(ir.DocumentStore, IRDSId):
    CONVERTERS = {
        GenericDoc: tuple_constructor(GenericDocument, "doc_id", "text"),
        _irds.beir.BeirCordDoc: tuple_constructor(
            formats.CordDocument, "doc_id", "text", "title", "url", "pubmed_id"
        ),
        _irds.beir.BeirTitleDoc: tuple_constructor(
            formats.TitleDocument, "doc_id", "text", "title"
        ),
        _irds.beir.BeirTitleUrlDoc: tuple_constructor(
            formats.TitleUrlDocument, "doc_id", "text", "title", "url"
        ),
        _irds.msmarco_document.MsMarcoDocument: tuple_constructor(
            formats.MsMarcoDocument, "doc_id", "url", "title", "body"
        ),
        _irds.cord19.Cord19FullTextDoc: tuple_constructor(
            formats.CordFullTextDocument,
            "doc_id",
            "title",
            "doi",
            "date",
            "abstract",
            "body",
        ),
        _irds.nfcorpus.NfCorpusDoc: tuple_constructor(
            formats.NFCorpusDocument, "doc_id", "url", "title", "abstract"
        ),
        TrecParsedDoc: tuple_constructor(
            formats.TrecParsedDocument, "doc_id", "title", "body", "marked_up_doc"
        ),
        _irds.wapo.WapoDoc: tuple_constructor(
            formats.WapoDocument, "doc_id", "url", "title", "author", "published_date", "kicker", "body", "body_paras_html", "body_media"
        ),
        _irds.tweets2013_ia.TweetDoc: tuple_constructor(
            formats.TweetDoc, "doc_id", "text", "user_id", "created_at", "lang", "reply_doc_id", "retweet_doc_id", "source", "source_content_type"
        )
    }

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
        return self.converter.target_cls

    @cached_property
    def converter(self):
        converter = Documents.CONVERTERS[self.dataset.docs_cls()]
        converter.check(self.dataset.docs_cls())
        return converter


@attrs.define()
class IRDSQueryWrapper(ir.Topic):
    query: Any


class Topics(ir.TopicsStore, IRDSId):
    CONVERTERS = {
        GenericQuery: tuple_constructor(GenericTopic, "query_id", "text"),
        _irds.beir.BeirCovidQuery: tuple_constructor(
            formats.TrecTopic, "query_id", "text", "query", "narrative"
        ),
        _irds.beir.BeirUrlQuery: tuple_constructor(
            formats.UrlTopic, "query_id", "text", "url"
        ),
        _irds.nfcorpus.NfCorpusQuery: tuple_constructor(
            formats.NFCorpusTopic, "query_id", "title", "all"
        ),
        TrecQuery: tuple_constructor(
            formats.TrecQuery, "query_id", "title", "description", "narrative"
        ),
        _irds.tweets2013_ia.TrecMb13Query: tuple_constructor(
            formats.TrecMb13Query, "query_id", "query", "time", "tweet_time"
        ),
        _irds.tweets2013_ia.TrecMb14Query: tuple_constructor(
            formats.TrecMb14Query, "query_id", "query", "time", "tweet_time", "description"
        )
    }

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
        return self.converter.target_cls

    @cached_property
    def converter(self):
        converter = Topics.CONVERTERS[self.dataset.queries_cls()]
        converter.check(self.dataset.queries_cls())
        return converter


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


if __name__ == "__main__":
    from datamaestro import prepare_dataset

    dataset = prepare_dataset("irds.wapo.v2.trec-core-2018")

    test = next(dataset.topics.iter())

    print()
