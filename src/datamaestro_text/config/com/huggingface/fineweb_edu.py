"""HuggingFaceFW/fineweb-edu — quality-filtered English web text.

A high-quality English web corpus shipped as parquet shards. Heavily
used as a substitute for / complement to DCLM in mid-2025 pretraining
recipes. Available subsets:

* ``sample/10BT``  — 14 parquet files (~30 GB, ~10 B tokens)
* ``sample/100BT`` — 140 parquet files (~286 GB, ~100 B tokens)
* ``sample/350BT`` — 472 parquet files (~1 TB, ~350 B tokens)

On HPC clusters such as Jean-Zay (IDRIS) this corpus is already
mirrored under ``$DSDIR/HuggingFace/HuggingFaceFW/fineweb-edu/``;
exporting ``DATAMAESTRO_HF_DATASETS_CACHE=$DSDIR/HuggingFace`` makes
``datamaestro prepare`` resolve the shards locally at zero quota cost.
"""

from datamaestro.definitions import Dataset, dataset, datatags, datatasks
from datamaestro.download.huggingface import HFSnapshotDownloader

from datamaestro_text.data.text import ParquetStreamingTextDataset


_REPO = "HuggingFaceFW/fineweb-edu"


@datatasks("language modeling", "distillation")
@datatags("english", "pretraining", "fineweb-edu", "web", "smoke")
@dataset(
    url="https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu",
    size="~57 MB",
)
class Smoke(Dataset):
    """Single small parquet shard of fineweb-edu for pipeline checks."""

    SHARDS = HFSnapshotDownloader.apply(
        "shards",
        repo_id=_REPO,
        repo_type="dataset",
        # Smallest single parquet in the repo (~57 MB).
        allow_patterns=["sample/350BT/016_00000.parquet"],
    )

    def config(self) -> ParquetStreamingTextDataset:
        return ParquetStreamingTextDataset.C(path=self.SHARDS.path)


@datatasks("language modeling", "distillation")
@datatags("english", "pretraining", "fineweb-edu", "web")
@dataset(
    url="https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu",
    size="~30 GB",
)
class Sample10b(Dataset):
    """``sample/10BT`` — 14 parquet shards, ~10 B tokens."""

    SHARDS = HFSnapshotDownloader.apply(
        "shards",
        repo_id=_REPO,
        repo_type="dataset",
        allow_patterns=["sample/10BT/*.parquet"],
    )

    def config(self) -> ParquetStreamingTextDataset:
        return ParquetStreamingTextDataset.C(path=self.SHARDS.path)


@datatasks("language modeling", "distillation")
@datatags("english", "pretraining", "fineweb-edu", "web")
@dataset(
    url="https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu",
    size="~286 GB",
)
class Sample100b(Dataset):
    """``sample/100BT`` — 140 parquet shards, ~100 B tokens."""

    SHARDS = HFSnapshotDownloader.apply(
        "shards",
        repo_id=_REPO,
        repo_type="dataset",
        allow_patterns=["sample/100BT/*.parquet"],
    )

    def config(self) -> ParquetStreamingTextDataset:
        return ParquetStreamingTextDataset.C(path=self.SHARDS.path)


@datatasks("language modeling", "distillation")
@datatags("english", "pretraining", "fineweb-edu", "web")
@dataset(
    url="https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu",
    size="~1 TB",
)
class Sample350b(Dataset):
    """``sample/350BT`` — 472 parquet shards, ~350 B tokens."""

    SHARDS = HFSnapshotDownloader.apply(
        "shards",
        repo_id=_REPO,
        repo_type="dataset",
        allow_patterns=["sample/350BT/*.parquet"],
    )

    def config(self) -> ParquetStreamingTextDataset:
        return ParquetStreamingTextDataset.C(path=self.SHARDS.path)
