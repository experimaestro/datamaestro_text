from typing import ClassVar
from attrs import define
from .base import IDHolder, Document, GenericTopic


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
        return f"{self.query}"


@define
class UrlTopic(GenericTopic):
    text: str
    url: str

    def get_text(self):
        return f"{self.text}"
    