from typing import ClassVar, Tuple
from attrs import define
from datamaestro.record import recordtypes
from ir_datasets.datasets.wapo import WapoDocMedia
from .base import TextItem, SimpleTextItem, IDTopicRecord
from ir_datasets.datasets.cord19 import Cord19FullTextSection


@define
class CordDocument(TextItem):
    text: str
    title: str
    url: str
    pubmed_id: str

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.title} {self.text}"


@define
class DocumentWithTitle(TextItem):
    """Web document with title and URL"""

    title: str

    text: str


@define
class CordFullTextDocument(TextItem):
    title: str
    doi: str
    date: str
    abstract: str
    body: Tuple[Cord19FullTextSection, ...]

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.abstract}"


@define
class MsMarcoDocument(TextItem):
    url: str
    title: str
    body: str

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.body}"


@define
class NFCorpusDocument(TextItem):
    url: str
    title: str
    abstract: str

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.abstract}"


@define
class TitleDocument(TextItem):
    text: str
    title: str
    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.title} {self.text}"


@define
class TitleUrlDocument(TextItem):
    text: str
    title: str
    url: str
    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.title} {self.text}"


@define
class TrecParsedDocument(TextItem):
    title: str
    body: str
    marked_up_doc: bytes

    has_text: ClassVar[bool] = True

    def get_text(self):
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

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.body}"


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

    def get_text(self):
        return f"{self.text}"


@define
class OrConvQADocument(TextItem):
    id: str
    title: str
    text: str
    aid: str
    bid: int

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.title} {self.text}"


@define
class TrecTopic(TextItem):
    text: str
    query: str
    narrative: str

    def get_text(self):
        return f"{self.text}"


@define
class UrlTopic(TextItem):
    text: str
    url: str

    def get_text(self):
        return f"{self.text}"


@define
class NFCorpusTopic(TextItem):
    title: str
    all: str

    def get_text(self):
        return f"{self.title}"


@define
class TrecQuery(TextItem):
    title: str
    description: str
    narrative: str

    def get_text(self):
        return f"{self.description}"


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
