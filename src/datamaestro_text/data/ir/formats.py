from typing import ClassVar, Tuple
from attrs import define
from .base import IDHolder, Document, GenericTopic
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
    