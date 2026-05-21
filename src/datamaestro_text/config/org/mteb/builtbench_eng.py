"""Pre-populated HF datasets cache for the ``BuiltBench(eng)`` benchmark.

The smallest English MTEB benchmark — 4 tasks. Useful as a fast eval
target before committing to the full ``MTEB(eng, v2)`` cache.
"""

import mteb

from datamaestro.definitions import Dataset, dataset, datatags, datatasks

from datamaestro_text.data.text import MTEBBenchmarkCache
from datamaestro_text.download.mteb import MTEBBenchmarkDownloader


_TASK_NAMES = [t.metadata.name for t in mteb.get_benchmark("BuiltBench(eng)").tasks]


@datatasks("evaluation", "sentence embeddings", "retrieval")
@datatags("english", "mteb", "benchmark", "builtbench")
@dataset(
    url="https://github.com/embeddings-benchmark/mteb",
    size="~few hundred MB",
)
class Cache(Dataset):
    """Pre-fetched HF datasets for every task in ``BuiltBench(eng)``."""

    DATA = MTEBBenchmarkDownloader.apply("data", task_names=_TASK_NAMES)

    def config(self) -> MTEBBenchmarkCache:
        return MTEBBenchmarkCache.C(path=self.DATA.path, task_names=_TASK_NAMES)
