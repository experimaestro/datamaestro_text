from csv import DictReader
from typing import Iterator

from datamaestro.data import File, documentation
from datamaestro_text.data.ir import (
    AdhocDocument,
    AdhocDocuments,
    AdhocTopic,
    AdhocTopics,
)
from datamaestro.data.csv import Generic as GenericCSV
import xml.etree.ElementTree as ET


class Topics(AdhocTopics, File):
    """XML format used in Adhoc topics"""

    def iter(self) -> Iterator[AdhocTopic]:
        """Returns an iterator over topics"""
        tree = ET.parse(self.path)
        for topic in tree.findall("topic"):
            yield AdhocTopic(
                topic.get("number"),
                topic.find("query").text,
                {
                    "question": topic.find("question").text,
                    "narrative": topic.find("narrative").text,
                },
            )


class Documents(AdhocDocuments, GenericCSV):
    @documentation
    def iter(self) -> Iterator[AdhocDocument]:
        """Returns an iterator over adhoc documents"""
        with self.path.open("r") as fp:
            for row in DictReader(fp):
                yield AdhocDocument(
                    row["cord_uid"], f"""{row["title"]} {row["abstract"]}"""
                )
