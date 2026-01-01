"""Data classes for the Grand Débat National dataset"""

import json
from dataclasses import dataclass, field
from typing import Iterator, List, Optional

from datamaestro.data import File


@dataclass
class GrandDebatResponse:
    """A response to a question in the Grand Débat National"""

    question_id: str
    question_title: str
    value: Optional[str]
    formatted_value: Optional[str]


@dataclass
class GrandDebatEntry:
    """An entry (contribution) in the Grand Débat National dataset"""

    id: str
    reference: str
    title: str
    created_at: str
    published_at: str
    updated_at: Optional[str]
    trashed: bool
    trashed_status: Optional[str]
    author_id: str
    author_type: str
    author_zip_code: str
    responses: List[GrandDebatResponse] = field(default_factory=list)


class GrandDebatFile(File):
    """A Grand Débat National JSONL file with iteration support"""

    def __iter__(self) -> Iterator[GrandDebatEntry]:
        """Iterate over entries in the JSONL file"""
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                responses = [
                    GrandDebatResponse(
                        question_id=r["questionId"],
                        question_title=r["questionTitle"],
                        value=r.get("value"),
                        formatted_value=r.get("formattedValue"),
                    )
                    for r in data.get("responses", [])
                ]
                yield GrandDebatEntry(
                    id=data["id"],
                    reference=data["reference"],
                    title=data["title"],
                    created_at=data["createdAt"],
                    published_at=data["publishedAt"],
                    updated_at=data.get("updatedAt"),
                    trashed=data["trashed"],
                    trashed_status=data.get("trashedStatus"),
                    author_id=data["authorId"],
                    author_type=data["authorType"],
                    author_zip_code=data["authorZipCode"],
                    responses=responses,
                )
