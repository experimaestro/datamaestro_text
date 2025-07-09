import json
from pathlib import Path
from typing import List, NamedTuple
from experimaestro import Constant, Meta
from datamaestro.utils import FileChecker
from datamaestro.record import Record
from datamaestro_text.data.ir.base import (
    DocumentRecord,
    IDItem,
    SimpleTextItem,
    TextItem,
    UrlItem,
)
from datamaestro_text.datasets.irds.data import LZ4DocumentStore
from datamaestro_text.data.ir.formats import OrConvQADocument


class OrConvQADocumentStore(LZ4DocumentStore):
    class NAMED_TUPLE(NamedTuple):
        id: str
        title: str
        body: str
        aid: str
        bid: int

    lookup_field: Constant[str] = "id"
    fields: Constant[List[str]] = list(NAMED_TUPLE._fields)
    index_fields: Constant[List[str]] = ["id"]

    data_cls = NAMED_TUPLE

    def converter(self, data: NAMED_TUPLE) -> Record:
        fields = data._asdict()
        del fields["id"]
        return Record(OrConvQADocument(**fields), IDItem(data.id))


def jsonl_reader(
    path: Path,
    suffix: str,
    *,
    opener: open,
    num_files: int | None = None,
    checker: FileChecker | None = None,
):
    """Read a set of JSONL files

    :param path: The path of the folder containing the files
    :param suffix: The suffix for the files to process
    :param opener: The opener (can be e.g. bz2.open to process bz2 files)
    :param num_files: Check that the number of files is num_file if provided, defaults to None
    :param checker: File content checker, defaults to None
    :yield: objects corresponding to the JSON of each line
    """
    # Get the file paths (and check their number)
    write = checker.write
    paths = list(path.glob(f"*{suffix}"))
    assert num_files is None or len(paths) == num_files, (
        f"The number of files in {path} ({len(paths)})"
        f" does not match what was expected ({num_files})"
    )

    # Process all the paths
    for path in paths:
        with opener(path, "rt") as fp:
            for ix, line in enumerate(fp):
                if checker is not None:
                    write(line.encode("utf-8"))
                yield json.loads(line)

    # Close the checker if it was opened
    if checker is not None:
        checker.close()


class IKatClueWeb22DocumentStore(LZ4DocumentStore):
    @staticmethod
    def generator(
        path: Path,
        suffix: str,
        *,
        opener: open,
        num_files: int | None = None,
        checker: FileChecker | None = None,
    ):
        def __iter__():
            iterator = jsonl_reader(
                path, suffix, opener=opener, checker=checker, num_files=num_files
            )
            yield from map(
                lambda data, *_: IKatClueWeb22DocumentStore.Document(**data), iterator
            )

        return __iter__

    class Document(NamedTuple):
        id: str
        contents: str
        url: str

    data_cls = Document
    lookup_field: Constant[str] = "id"
    index_fields: Constant[List[str]] = ["id"]

    def converter(self, data):
        return DocumentRecord(
            IDItem(data.id), SimpleTextItem(data.contents), UrlItem(data.url)
        )
