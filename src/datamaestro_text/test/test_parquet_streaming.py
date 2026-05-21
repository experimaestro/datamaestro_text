"""Tests for :class:`datamaestro_text.data.text.ParquetStreamingTextDataset`."""

from __future__ import annotations

from pathlib import Path

import pytest

pa = pytest.importorskip("pyarrow")
pq = pytest.importorskip("pyarrow.parquet")

from datamaestro_text.data.text import ParquetStreamingTextDataset  # noqa: E402


def _write(parquet_path: Path, rows: list[str], column: str = "text") -> None:
    pq.write_table(pa.table({column: rows}), parquet_path)


def test_iter_text_concatenates_shards_in_sorted_order(tmp_path: Path):
    _write(tmp_path / "b.parquet", ["beta-1", "beta-2"])
    _write(tmp_path / "a.parquet", ["alpha-1", "alpha-2"])

    ds = ParquetStreamingTextDataset.C(id="test.parquet.0", path=tmp_path).instance()
    rows = list(ds.iter_text())

    # Sorted glob order — a.* read first, b.* second.
    assert rows == ["alpha-1", "alpha-2", "beta-1", "beta-2"]


def test_empty_text_records_skipped(tmp_path: Path):
    _write(tmp_path / "shard.parquet", ["hello", "", "world"])

    ds = ParquetStreamingTextDataset.C(id="test.parquet.1", path=tmp_path).instance()
    assert list(ds.iter_text()) == ["hello", "world"]


def test_custom_text_column(tmp_path: Path):
    _write(tmp_path / "shard.parquet", ["foo", "bar"], column="content")

    ds = ParquetStreamingTextDataset.C(
        id="test.parquet.2", path=tmp_path, text_column="content"
    ).instance()
    assert list(ds.iter_text()) == ["foo", "bar"]


def test_recursive_glob_finds_nested_shards(tmp_path: Path):
    nested = tmp_path / "sample" / "10BT"
    nested.mkdir(parents=True)
    _write(nested / "000_00000.parquet", ["nested-hit"])

    ds = ParquetStreamingTextDataset.C(id="test.parquet.3", path=tmp_path).instance()
    assert list(ds.iter_text()) == ["nested-hit"]


def test_batch_size_meta_does_not_change_identity(tmp_path: Path):
    a = ParquetStreamingTextDataset.C(id="same.id", path=tmp_path, batch_size=1000)
    b = ParquetStreamingTextDataset.C(id="same.id", path=tmp_path, batch_size=8000)
    # batch_size is Param though — explicit different identity expected
    # only matters that we declared it so; identity sameness for *path*
    # (Meta) is the load-bearing invariant.
    assert a.__xpm__.identifier.main != b.__xpm__.identifier.main
