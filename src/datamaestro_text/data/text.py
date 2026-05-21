from typing import Iterator, Optional
from experimaestro import Param
from datamaestro.data import Base, Folder, File
from datamaestro.data.ml import Supervised


class TrainingText(Supervised):
    """ "A dataset used for training with a train and a test"""

    train: Param[Base]
    test: Param[Optional[Base]] = None
    validation: Param[Optional[Base]] = None


class TextFolder(Folder):
    "A folder composed of texts"

    pass


class TextFile(File):
    """A file composed of texts"""

    pass


class StreamingTextDataset(Folder):
    """A text corpus organised for streaming consumption.

    The directory holds one or more ``.jsonl.tar.gz`` shards. Each shard
    decompresses to a JSONL file whose lines are JSON objects with a
    ``"text"`` field carrying a single text record (a document or a
    fixed-length chunk, depending on how the corpus was prepared).

    Subclass and override :meth:`iter_text` if a different on-disk
    format is needed. The default implementation has only stdlib
    dependencies (``json`` + ``tarfile``).
    """

    def iter_text(self) -> Iterator[str]:
        """Stream the ``"text"`` field across all ``.jsonl.tar.gz`` shards."""
        import json
        import tarfile

        for shard in sorted(self.path.glob("**/*.jsonl.tar.gz")):
            with tarfile.open(shard, "r:gz") as tar:
                for member in tar:
                    if not member.isfile():
                        continue
                    fobj = tar.extractfile(member)
                    if fobj is None:
                        continue
                    for line in fobj:
                        try:
                            record = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        text = record.get("text")
                        if text:
                            yield text
