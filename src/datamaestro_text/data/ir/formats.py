from functools import cached_property
from typing import ClassVar, Tuple
from attrs import define
from datamaestro.record import recordtypes
from ir_datasets.datasets.wapo import WapoDocMedia
from .base import TextItem, SimpleTextItem, IDTopicRecord
from ir_datasets.datasets.cord19 import Cord19FullTextSection


@define
class DocumentWithTitle(TextItem):
    """Web document with title and body"""

    body: str

    title: str

    @cached_property
    def text(self):
        return f"{self.title} {self.body}"


@define
class CordDocument(DocumentWithTitle):
    url: str
    pubmed_id: str


@define
class CordFullTextDocument(TextItem):
    title: str
    doi: str
    date: str
    abstract: str
    body: Tuple[Cord19FullTextSection, ...]

    @cached_property
    def text(self):
        return self.abstract


@define
class MsMarcoDocument(TextItem):
    url: str
    title: str
    body: str

    @cached_property
    def text(self):
        return self.body


@define
class NFCorpusDocument(TextItem):
    url: str
    title: str
    abstract: str

    @cached_property
    def text(self):
        return self.abstract


@define
class TitleDocument(TextItem):
    body: str
    title: str

    @cached_property
    def text(self):
        return f"{self.title} {self.body}"


@define
class TitleUrlDocument(TitleDocument):
    url: str


@define
class TrecParsedDocument(TextItem):
    title: str
    body: str
    marked_up_doc: bytes

    @cached_property
    def text(self):
        return f"{self.title} {self.body}"


@define
class WapoDocument(TextItem):
    url: str
    title: str
    author: str
    published_date: int
    kicker: str
    body: str
    body_paras_html: Tuple[str, ...]
    body_media: Tuple[WapoDocMedia, ...]

    @cached_property
    def text(self):
        return self.body


@define
class TweetDoc(TextItem):
    text: str
    user_id: str
    created_at: str
    lang: str
    reply_doc_id: str
    retweet_doc_id: str
    source: bytes
    source_content_type: str


@define
class OrConvQADocument(TextItem):
    id: str
    title: str
    body: str
    aid: str
    bid: int

    @cached_property
    def text(self):
        return f"{self.title} {self.body}"


@define
class TrecTopic(TextItem):
    text: str
    query: str
    narrative: str


@define
class UrlTopic(TextItem):
    text: str
    url: str


@define
class NFCorpusTopic(TextItem):
    text: str
    all: str


@define
class TrecMb13Query(TextItem):
    query: str
    time: str
    tweet_time: str

    def get_text(self):
        return f"{self.query}"


@define
class TrecMb14Query(TextItem):
    query: str
    time: str
    tweet_time: str
    description: str

    def get_text(self):
        return f"{self.query}"


@define()
class TrecTopic(SimpleTextItem):
    description: str
    narrative: str


@recordtypes(TrecTopic)
class TrecTopicRecord(IDTopicRecord):
    ...
