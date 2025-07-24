import bz2
from hashlib import md5, sha256
import json
import logging
from pathlib import Path
from typing import List, NamedTuple
from datamaestro_text.utils.files import TQDMFileReader
from experimaestro import Constant
from datamaestro.record import Record
from datamaestro_text.data.ir.base import (
    DocumentRecord,
    IDItem,
    SimpleTextItem,
    UrlItem,
)
from datamaestro_text.datasets.irds.data import LZ4DocumentStore
from datamaestro_text.data.ir.formats import OrConvQADocument
from tqdm import tqdm


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


class IKatClueWeb22DocumentStore(LZ4DocumentStore):
    @staticmethod
    def generator(path: Path, checksums_file: Path, passages_hashes: Path):
        """Returns an iterator over iKAT 2022-25 documents

        :param path: The folder containing the files
        """

        def __iter__():
            errors = False

            assert checksums_file.is_file(), f"{checksums_file} does not exist"
            assert passages_hashes.is_file(), f"{passages_hashes} does not exist"

            # Get the list of files
            with checksums_file.open("rt") as fp:
                files = []
                for line in fp:
                    checksum, filename = line.strip().split()
                    files.append((checksum, filename))
                    if not (path / filename).is_file():
                        logging.error("File %s does not exist", path / filename)
                        errors = True

            assert not errors, "Errors detected, stopping"

            # Check the SHA256 sums
            match checksums_file.suffix:
                case ".sha256sums":
                    hasher_factory = sha256
                case _:
                    raise NotImplementedError(
                        f"Cannot handle {checksums_file.suffix} checksum files"
                    )

            for checksum, filename in tqdm(files):
                logging.info("Checking %s", filename)
                hasher = hasher_factory()
                with (path / filename).open("rb") as fp:
                    while data := fp.read(2**20):
                        hasher.update(data)

                file_checksum = hasher.hexdigest()
                assert file_checksum == checksum, (
                    f"Expected {checksum}, " f"got {file_checksum} for {filename}"
                )

            # Get the MD5 hashes of all the passages
            logging.info("Reading the hashes of all passages")
            with TQDMFileReader(passages_hashes, "rt", bz2.open) as fp:
                passage_checksums = {}
                for line in tqdm(fp):
                    doc_id, passage_no, checksum = line.strip().split()
                    passage_checksums[f"{doc_id}:{passage_no}"] = checksum  # noqa: E231

            # Read the files
            logging.info("Starting to read the files")
            for _, filename in tqdm(files):
                with TQDMFileReader(path / filename, "rt", bz2.open) as jsonl_fp:
                    for line in jsonl_fp:
                        data = json.loads(line)
                        expected = passage_checksums[data["id"]]
                        computed = md5(data["contents"].encode("utf-8")).hexdigest()
                        assert expected == computed, (
                            f"Expected {expected}, "
                            f"got {computed} for passage {data['id']} in {filename}"
                        )
                        yield IKatClueWeb22DocumentStore.Document(**data)

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
