"""Ettin pretraining corpus (JHU-CLSP).

The Ettin model suite is distributed with its pretraining data at
``jhu-clsp/ettin-pretraining-data``. Phase 1 is 1.7T tokens organised in
several subfolders (DCLM ~49 %, CC head ~21 %, Starcoder ~15.5 %, plus
smaller text/code/math sources). Each subfolder holds one or more
``.jsonl.tar.gz`` archives. Each JSONL record is a JSON object with an
``id``, a ``text`` field (the raw text — already chunked to fit a 1024-token
window under the Ettin tokeniser), and a ``domain`` field. The "tokenized"
in the filename refers to the *chunking target*, not the on-disk format.

We register two variants here:

* :class:`Smoke` — a single tiny DCLM shard (~7 MB) for pipeline
  correctness checks on a laptop.
* :class:`DCLM` — the full DCLM subfolder. ~800 GB on disk and the natural
  starting point for real distillation runs.

Both datasets return a :class:`~datamaestro_text.data.text.StreamingTextDataset`;
consumers iterate raw text via ``iter_text()`` and tokenise downstream.
"""

from datamaestro.definitions import Dataset, dataset, datatags, datatasks
from datamaestro.download.huggingface import HFSnapshotDownloader

from datamaestro_text.data.text import StreamingTextDataset


_REPO = "jhu-clsp/ettin-pretraining-data"


@datatasks("language modeling", "distillation")
@datatags("english", "pretraining", "ettin")
@dataset(
    url="https://huggingface.co/datasets/jhu-clsp/ettin-pretraining-data",
    size="~7 MB",
)
class Smoke(Dataset):
    """Smoke-test slice of the Ettin pretraining corpus.

    Downloads one ~7 MB DCLM shard. Sufficient to exercise the data → model
    pipeline; **not** representative of the full corpus distribution.
    """

    _SHARD_STEM = (
        "mlfoundations-dclm-baseline-1.0-parquet-sampled-v3/"
        "split_97914-tokenized-chunked-1024-512-128-backfill-nodups"
    )

    SHARDS = HFSnapshotDownloader.apply(
        "shards",
        repo_id=_REPO,
        repo_type="dataset",
        allow_patterns=[
            f"{_SHARD_STEM}.jsonl.tar.gz",
            f"{_SHARD_STEM}.log",
        ],
    )

    def config(self) -> StreamingTextDataset:
        return StreamingTextDataset.C(path=self.SHARDS.path)


@datatasks("language modeling", "distillation")
@datatags("english", "pretraining", "ettin", "dclm")
@dataset(
    url="https://huggingface.co/datasets/jhu-clsp/ettin-pretraining-data",
    size="~800 GB",
)
class DCLM(Dataset):
    """Full DCLM subfolder of the Ettin Phase-1 mixture (837 B tokens).

    DCLM is 49 % of the original mix. Downloads every
    ``mlfoundations-dclm-baseline-1.0-parquet-sampled*/split_*.jsonl.tar.gz``
    file — substantial disk and bandwidth.
    """

    SHARDS = HFSnapshotDownloader.apply(
        "shards",
        repo_id=_REPO,
        repo_type="dataset",
        allow_patterns=[
            "mlfoundations-dclm-baseline-1.0-parquet-sampled*/*.jsonl.tar.gz",
        ],
    )

    def config(self) -> StreamingTextDataset:
        return StreamingTextDataset.C(path=self.SHARDS.path)
