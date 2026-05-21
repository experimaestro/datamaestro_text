"""Tiny MTEB cache for pipeline smoke tests.

Single task — ``STS12`` (mteb/sts12-sts) — chosen for being one of the
smallest English STS tasks (a few MB on disk). Sufficient to verify the
eval task end-to-end without committing to a real benchmark download.
"""

from datamaestro.definitions import Dataset, dataset, datatags, datatasks

from datamaestro_text.data.text import MTEBBenchmarkCache
from datamaestro_text.download.mteb import MTEBBenchmarkDownloader


_TASK_NAMES = ["STS12"]


@datatasks("evaluation", "sentence embeddings", "smoke")
@datatags("english", "mteb", "sts", "smoke")
@dataset(
    url="https://github.com/embeddings-benchmark/mteb",
    size="~few MB",
)
class Cache(Dataset):
    """Single-task MTEB cache for smoke tests (``STS12`` only)."""

    DATA = MTEBBenchmarkDownloader.apply("data", task_names=_TASK_NAMES)

    def config(self) -> MTEBBenchmarkCache:
        return MTEBBenchmarkCache.C(path=self.DATA.path, task_names=_TASK_NAMES)
