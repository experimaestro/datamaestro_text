from csv import DictReader
from typing import Iterator

from datamaestro.data import File, documentation
from datamaestro_text.data.ir import (
    Document,
    Documents,
    Topic,
    Topics,
)
from datamaestro.data.csv import Generic as GenericCSV
import xml.etree.ElementTree as ET


class Topics(Topics, File):
    """XML format used in Adhoc topics"""

    def iter(self) -> Iterator[Topic]:
        """Returns an iterator over topics"""
        tree = ET.parse(self.path)
        for topic in tree.findall("topic"):
            yield Topic(
                topic.get("number"),
                topic.find("query").text,
                {
                    "question": topic.find("question").text,
                    "narrative": topic.find("narrative").text,
                },
            )


class Documents(Documents, GenericCSV):
    @documentation
    def iter(self) -> Iterator[Document]:
        """Returns an iterator over adhoc documents"""
        with self.path.open("r") as fp:
            for row in DictReader(fp):
                yield Document(row["cord_uid"], f"""{row["title"]} {row["abstract"]}""")
