"""Pre-populated HF datasets cache for the ``MTEB(eng, v2)`` benchmark.

The task list is resolved at module-load time via :func:`mteb.get_benchmark`
so the resulting dataset identifier is stable as long as mteb's benchmark
composition doesn't change. The full cache can be tens of GB on disk.
"""

import mteb

from datamaestro.definitions import Dataset, dataset, datatags, datatasks

from datamaestro_text.data.text import MTEBBenchmarkCache
from datamaestro_text.download.mteb import MTEBBenchmarkDownloader


_TASK_NAMES = [t.metadata.name for t in mteb.get_benchmark("MTEB(eng, v2)").tasks]


@datatasks("evaluation", "sentence embeddings", "retrieval")
@datatags("english", "mteb", "benchmark")
@dataset(
    url="https://github.com/embeddings-benchmark/mteb",
    size="tens of GB",
)
class Cache(Dataset):
    """Pre-fetched HF datasets for every task in ``MTEB(eng, v2)``."""

    DATA = MTEBBenchmarkDownloader.apply("data", task_names=_TASK_NAMES)

    def config(self) -> MTEBBenchmarkCache:
        return MTEBBenchmarkCache.C(path=self.DATA.path, task_names=_TASK_NAMES)
