from pathlib import Path
from typing import Iterator, Optional
import re
from datamaestro_text.data.ir import AdhocRunDict
from datamaestro_text.data.ir.base import (
    AdhocAssessedTopic,
    TopicRecord,
    SimpleAdhocAssessment,
    IDItem,
)
from datamaestro_text.data.ir.formats import TrecTopicRecord, TrecTopic

# --- Runs


def parse_run(path: Path) -> AdhocRunDict:
    results = {}
    with path.open("rt") as f:
        for line in f:
            query_id, _q0, doc_id, _rank, score, _model_id = re.split(
                r"\s+", line.strip()
            )
            results.setdefault(query_id, {})[doc_id] = score

    return results


def write_run_dict(run: AdhocRunDict, run_path: Path):
    """Write run dict"""
    with run_path.open("wt") as f:
        for query_id, scored_documents in run.items():
            scored_documents = list(
                [(doc_id, score) for doc_id, score in scored_documents.items()]
            )
            scored_documents.sort(key=lambda x: x[1], reverse=True)
            for ix, (doc_id, score) in enumerate(scored_documents):
                f.write(f"{query_id} Q0 {doc_id} {ix + 1} {score} run\n")


# --- Assessments


def parse_qrels(path: Path) -> Iterator[AdhocAssessedTopic]:
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
            assessments.append(SimpleAdhocAssessment(docno, int(rel)))

        yield AdhocAssessedTopic(_qid, assessments)


# ---- TOPICS


def cleanup(s: Optional[str]) -> str:
    return s.replace("\t", " ").strip() if s is not None else ""


def parse_query_format(file, xml_prefix=None) -> Iterator[TopicRecord]:
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
                    yield TrecTopicRecord(
                        IDItem(num),
                        TrecTopic(cleanup(title), cleanup(desc), cleanup(narr)),
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
