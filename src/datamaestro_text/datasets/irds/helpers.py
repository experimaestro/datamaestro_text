import logging
from typing import Optional, Type, Callable, Iterator
from ir_datasets.indices import PickleLz4FullStore
from datamaestro.download import Download
from datamaestro.utils import FileChecker
from pathlib import Path
import urllib3


class lz4docstore_downloader(Download):
    """Uses ir_datasets Lz4FullStore to build a document store for a stream of documents"""

    def __init__(
        self,
        varname: str,
        url: str,
        iter_factory: Callable[[Path], Iterator],
        doc_cls: Type,
        lookup_field: str,
        *,
        count_hint: Optional[int] = None,
        size: Optional[int] = None,
        checker: FileChecker = None,
    ):
        super().__init__(varname)
        self.iter_factory = iter_factory
        self.url = url
        self.doc_cls = doc_cls
        self.size = size
        self.lookup_field = lookup_field
        self.count_hint = count_hint
        self.checker = checker

        p = urllib3.util.parse_url(self.url)
        assert p is not None
        self.name = Path(p.path).with_suffix("").name

    def prepare(self):
        return self.definition.datapath / self.name

    def download(self, force=False):
        # Creates directory if needed
        destination = self.definition.datapath / self.name
        destination.mkdir(exist_ok=True)

        # Early exit
        if (destination / "done").is_file() and not force:
            return True

        # Download (cache)
        logging.info("Building the document index")
        with self.context.downloadURL(self.url, size=self.size) as file:
            # Checks the file
            if self.checker:
                self.checker.check(file.path)

            # Builds the LZ4 store
            store = PickleLz4FullStore(
                destination,
                lambda: self.iter_factory(Path(file.path)),
                self.doc_cls,
                lookup_field=self.lookup_field,
                index_fields=[self.lookup_field],
                key_field_prefix=None,
                size_hint=None,
                count_hint=self.count_hint,
            )
            store.build()

            # All good!
            (destination / "done").touch()
