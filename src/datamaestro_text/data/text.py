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


class MTEBBenchmarkCache(Folder):
    """An HF datasets cache pre-populated for a chosen list of MTEB tasks.

    Consumers point ``HF_DATASETS_CACHE`` (or :func:`datasets.load_dataset`'s
    ``cache_dir``) at :attr:`path` and iterate the tasks named in
    :attr:`task_names` via :func:`mteb.get_task` — every dataset
    resolves locally without network access.

    Attributes:
        task_names: List of mteb task names (e.g.
            ``["STS12", "STS13", ...]``) covered by this cache.
    """

    task_names: Param[list[str]]


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
