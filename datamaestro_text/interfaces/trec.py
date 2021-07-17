from dataclasses import dataclass
from pathlib import Path
from typing import List, NamedTuple, Optional
import re

from datamaestro_text.data.ir import (
    AdhocAssessedTopic,
    AdhocAssessment,
    AdhocTopic,
)

# --- Assessments


def parse_qrels(path: Path):
    with path.open("rt") as fp:
        _qid = None
        assessments = []

        for line in fp:
            qid, _, docno, rel = re.split(r"\s+", line.strip())
            if qid != _qid:
                if _qid is not None:
                    yield AdhocAssessedTopic(_qid, assessments)
                _qid = qid
                assessments = []
            assessments.append(AdhocAssessment(docno, int(rel)))

        yield AdhocAssessedTopic(_qid, assessments)


# ---- TOPICS


@dataclass()
class TrecAdhocTopic(AdhocTopic):
    description: str
    narrative: str


def cleanup(s: Optional[str]) -> str:
    return s.replace("\t", " ").strip() if s is not None else ""


def parse_query_format(file, xml_prefix=None):
    """Parse TREC XML query format"""
    if xml_prefix is None:
        xml_prefix = ""

    if hasattr(file, "read"):
        num, title, desc, narr, reading = None, None, None, None, None
        for line in file:
            if line.startswith("**"):
                # translation comment in older formats (e.g., TREC 3 Spanish track)
                continue
            elif line.startswith("</top>"):
                if num:
                    yield TrecAdhocTopic(
                        num, cleanup(title), cleanup(desc), cleanup(narr)
                    )
                num, title, desc, narr, reading = None, None, None, None, None
            elif line.startswith("<num>"):
                num = line[len("<num>") :].replace("Number:", "").strip()
                reading = None
            elif line.startswith(f"<{xml_prefix}title>"):
                title = line[len(f"<{xml_prefix}title>") :].strip()
                if title == "":
                    reading = "title"
                else:
                    reading = None
            elif line.startswith(f"<{xml_prefix}desc>"):
                desc = ""
                reading = "desc"
            elif line.startswith(f"<{xml_prefix}narr>"):
                narr = ""
                reading = "narr"
            elif reading == "desc":
                desc += line.strip() + " "
            elif reading == "narr":
                narr += line.strip() + " "
            elif reading == "title":
                title += line.strip() + " "
    else:
        with open(file, "rt") as f:
            yield from parse_query_format(f)
