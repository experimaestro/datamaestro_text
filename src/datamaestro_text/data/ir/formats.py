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
class TrecTopic(GenericTopic):
    text: str
    query: str
    narrative: str

    def get_text(self):
        return f"{self.query}"
