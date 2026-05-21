"""MTEB benchmark cache downloader.

Materialises an HF datasets cache populated with the underlying HF
datasets for an explicit list of MTEB task names, so downstream
evaluation can run offline by pointing ``HF_DATASETS_CACHE`` at the
resulting directory.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from datamaestro.download import FolderResource

logger = logging.getLogger(__name__)


class MTEBBenchmarkDownloader(FolderResource):
    """Download HF datasets for a list of MTEB task names.

    Each name is resolved via :func:`mteb.get_task`; the task's
    underlying HF dataset (``task.metadata.dataset["path"]``) is fetched
    via :func:`datasets.load_dataset` with ``cache_dir`` set to the
    resource folder. ``mteb`` and ``datasets`` are imported lazily.

    Concrete dataset definitions typically compute the name list from a
    benchmark identifier at module-load time, e.g.::

        import mteb
        _TASKS = [t.metadata.name for t in mteb.get_benchmark("MTEB(eng, v2)").tasks]

        @dataset(...)
        class Cache(Dataset):
            DATA = MTEBBenchmarkDownloader.apply("data", task_names=_TASKS)
            def config(self) -> MTEBBenchmarkCache:
                return MTEBBenchmarkCache.C(path=self.DATA.path, task_names=_TASKS)
    """

    def __init__(
        self,
        varname: str,
        task_names: Iterable[str],
        *,
        transient: bool = False,
    ):
        super().__init__(varname=varname, transient=transient)
        self.task_names = list(task_names)

    def _download(self, destination: Path) -> None:
        try:
            import mteb
        except ModuleNotFoundError:
            logger.error("the mteb library is not installed")
            raise
        try:
            from datasets import load_dataset
        except ModuleNotFoundError:
            logger.error("the datasets library is not installed")
            raise

        destination.mkdir(parents=True, exist_ok=True)
        logger.info(
            "Downloading %d MTEB task datasets into %s",
            len(self.task_names),
            destination,
        )
        for name in self.task_names:
            try:
                task = mteb.get_task(name)
            except Exception:  # noqa: BLE001
                logger.exception("Cannot resolve mteb task %r; skipping", name)
                continue
            ds = task.metadata.dataset
            path = ds.get("path") if isinstance(ds, dict) else None
            if not path:
                logger.warning("Skipping task %s: no dataset path in metadata", name)
                continue
            revision = ds.get("revision") if isinstance(ds, dict) else None
            logger.info("Fetching task %s ← %s", name, path)
            try:
                load_dataset(path, revision=revision, cache_dir=str(destination))
            except Exception:  # noqa: BLE001
                logger.exception("Failed to fetch %s; continuing", name)
