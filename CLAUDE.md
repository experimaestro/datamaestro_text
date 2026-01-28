# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

datamaestro-text is a [datamaestro](https://github.com/bpiwowar/datasets) plugin that provides text-related datasets for Information Retrieval (IR) and Natural Language Processing (NLP) tasks.

## Build & Development Commands

```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest src/datamaestro_text

# Run a single test file
pytest src/datamaestro_text/test/test_datasets.py

# Linting and formatting
ruff check src/datamaestro_text
ruff format src/datamaestro_text

# Build documentation
make -C docs html
```

## Architecture

### Package Structure

- `src/datamaestro_text/` - Main package
  - `data/` - Data type definitions (schemas for datasets)
    - `ir/` - Information retrieval types: `Documents`, `Topics`, `AdhocAssessments`, `Adhoc`, `TrainingTriplets`
    - `conversation/` - Conversational IR types
    - `text.py`, `embeddings.py`, `recommendation.py` - Other data types
  - `config/` - Dataset definitions organized by domain (mirrors URL structure)
    - e.g., `config/com/microsoft/msmarco/` for MS-MARCO datasets
  - `datasets/irds/` - Integration with [ir_datasets](https://ir-datasets.com/)
  - `utils/` - Utility functions
  - `transforms/` - Data transformations

### Plugin System

The repository is registered as a datamaestro plugin via entry points in `pyproject.toml`:
- `text` namespace: Main repository (`datamaestro_text:Repository`)
- `irds` namespace: ir_datasets integration (`datamaestro_text.datasets.irds:Repository`)

### Dataset Definition Pattern

Datasets are defined using decorators in `config/` modules:
```python
@filedownloader("file.tsv", url="...", checker=HashCheck("...", md5))
@dataset(DataType, url="...")
def dataset_name(file):
    return {"path": file, ...}
```

Key decorators:
- `@dataset(DataType)` - Declares the dataset type
- `@filedownloader`, `@tardownloader` - Download handlers
- `@reference("name", other_dataset)` - Links to other datasets
- `@datatasks("task1", "task2")` - Task categorization
- `@useragreement(...)` - User agreement requirements

### Key Data Types (in `data/ir/`)

- `Documents` - Collection of documents with IDs
- `DocumentStore` - Documents with random access by ID
- `Topics` - Query/topic collection
- `AdhocAssessments` - Relevance judgments (qrels)
- `Adhoc` - Complete IR dataset (documents + topics + assessments)
- `TrainingTriplets` - Training data (query, positive doc, negative doc)

### Record System

Uses `datamaestro.record` for typed records with items like `IDItem`, `TextItem`. Records are created via `record_type()` and item classes.
