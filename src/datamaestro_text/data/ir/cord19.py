from csv import DictReader
from typing import Iterator

from datamaestro.data import File, documentation
from datamaestro.record import Record
from datamaestro_text.data.ir import Documents, TopicRecord, Topics, IDItem
from datamaestro_text.data.ir.formats import (
    DocumentWithTitle,
    TrecTopicRecord,
    TrecTopic,
)
from datamaestro.data.csv import Generic as GenericCSV
import xml.etree.ElementTree as ET


class Topics(Topics, File):
    """XML format used in Adhoc topics"""

    def iter(self) -> Iterator[TopicRecord]:
        """Returns an iterator over topics"""
        tree = ET.parse(self.path)
        for topic in tree.findall("topic"):
            yield TrecTopicRecord(
                IDItem(topic.get("number")),
                TrecTopic(
                    topic.find("query").text,
                    question=topic.find("question").text,
                    narrative=topic.find("narrative").text,
                ),
            )

    @property
    def topic_recordtype(self):
        return TrecTopicRecord


class Documents(Documents, GenericCSV):
    @documentation
    def iter(self) -> Iterator[Record]:
        """Returns an iterator over adhoc documents"""
        with self.path.open("r") as fp:
            for row in DictReader(fp):
                yield Record(
                    IDItem(row["cord_uid"]),
                    DocumentWithTitle(row["abstract"], row["title"]),
                )
