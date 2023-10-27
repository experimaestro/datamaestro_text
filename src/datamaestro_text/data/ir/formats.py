from typing import ClassVar, Tuple
from attrs import define
from ir_datasets.datasets.wapo import WapoDocMedia
from .base import IDHolder, Document, GenericTopic, IDTopic
from ir_datasets.datasets.cord19 import Cord19FullTextSection


@define
class CordDocument(IDHolder, Document):
    text: str
    title: str
    url: str
    pubmed_id: str

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.title} {self.text}"


@define
class DocumentWithTitle(IDHolder, Document):
    """Web document with title and URL"""

    title: str

    text: str


@define
class CordFullTextDocument(IDHolder, Document):
    title: str
    doi: str
    date: str
    abstract: str
    body: Tuple[Cord19FullTextSection, ...]

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.abstract}"


@define
class MsMarcoDocument(IDHolder, Document):
    url: str
    title: str
    body: str

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.body}"


@define
class NFCorpusDocument(IDHolder, Document):
    url: str
    title: str
    abstract: str

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.abstract}"


@define
class TitleDocument(IDHolder, Document):
    text: str
    title: str
    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.title} {self.text}"


@define
class TitleUrlDocument(IDHolder, Document):
    text: str
    title: str
    url: str
    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.title} {self.text}"


@define
class TrecParsedDocument(IDHolder, Document):
    title: str
    body: str
    marked_up_doc: bytes

    has_text: ClassVar[bool] = True

    def get_text(self):
        return f"{self.title} {self.body}"


@define
class WapoDocument(IDHolder, Document):
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
class TweetDoc(IDHolder, Document):
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
class TrecTopic(GenericTopic):
    text: str
    query: str
    narrative: str

    def get_text(self):
        return f"{self.text}"


@define
class UrlTopic(GenericTopic):
    text: str
    url: str

    def get_text(self):
        return f"{self.text}"


@define
class NFCorpusTopic(IDTopic):
    title: str
    all: str

    def get_text(self):
        return f"{self.title}"


@define
class TrecQuery(IDTopic):
    title: str
    description: str
    narrative: str

    def get_text(self):
        return f"{self.description}"


@define
class TrecMb13Query(IDTopic):
    query: str
    time: str
    tweet_time: str

    def get_text(self):
        return f"{self.query}"


@define
class TrecMb14Query(IDTopic):
    query: str
    time: str
    tweet_time: str
    description: str

    def get_text(self):
        return f"{self.query}"
