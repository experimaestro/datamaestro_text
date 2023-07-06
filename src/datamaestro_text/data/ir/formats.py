from attrs import define
from .base import IDHolder, Document, Topic


@define
class CordDocument(IDHolder, Document):
    text: str
    title: str
    url: str
    pubmed_id: str


@define
class TrecTopic(IDHolder, Topic):
    text: str
    query: str
    narrative: str
