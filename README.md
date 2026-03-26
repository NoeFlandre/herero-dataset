# Herero Language Dataset

[![HuggingFace Dataset](https://img.shields.io/badge/Dataset-HuggingFace-blue)](https://huggingface.co/datasets/NoeFlandre/herero-dataset)

A **multi-license collection** of [Herero (Otjiherero)](https://en.wikipedia.org/wiki/Herero_language) text for NLP research and LLM pretraining.

**⚠️ This repository redistributes materials from multiple upstream sources under different licenses. Check per-row `original_license` before reuse.**

## Quick Start

```python
from datasets import load_dataset
dataset = load_dataset("NoeFlandre/herero-dataset")

# Check license BEFORE use
example = dataset["train"][0]
print(f"License: {example['original_license']}")
```

## Dataset Summary

| Metric | Value |
|--------|-------|
| Documents | 1,951 |
| Words | 870,941 |
| Sources | 7 |
| Language | Herero (hz) |

## Sources

| Source | Docs | Words | License |
|--------|-----:|------:|---------|
| FineWeb-2 | 1,272 | 672,378 | ODC-By 1.0 |
| Omnilingual ASR | 437 | 60,485 | CC BY 4.0 |
| GlotCC-V1 | 20 | 75,982 | CC BY 4.0 |
| Herero Bible (1849) | 81 | 26,807 | Public Domain |
| Storybooks Namibia | 46 | 13,246 | CC BY 4.0 |
| FinePDFs | 25 | 17,800 | ODC-By 1.0 |
| Wikipedia Incubator | 70 | 4,243 | CC BY-SA 3.0 |

## Data Splits

| Split | Documents |
|-------|-----------|
| train | 1,761 |
| validation | 95 |
| test | 95 |

## Schema

| Field | Description |
|-------|-------------|
| `id` | Unique document ID |
| `text` | Herero text (NFC normalized) |
| `source` | Data source name |
| `original_license` | **Check this before use!** |
| `original_url` | Link to original source |
| `changes_made` | Transformations applied |
| `license_type` | License category |

## Installation

```bash
uv sync  # or: pip install -r requirements.txt
pytest tests/ -v
```

## Project Structure

```
├── huggingface_dataset/   # Dataset on HF Hub
│   ├── README.md         # Dataset card
│   ├── LICENSE           # Multi-license notice
│   ├── sources.csv       # Source manifest
│   └── data/
│       ├── train.parquet
│       ├── validation.parquet
│       └── test.parquet
├── scripts/              # Scrapers & processing
├── tests/               # TDD tests
├── docs/                # Source documentation
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Classification

This is a **collection**, not an adaptation:
- Sources aggregated without material modification
- Original text preserved
- No cross-source merging or rewriting
- ShareAlike does not apply to mere collections

## License

See [huggingface_dataset/LICENSE](huggingface_dataset/LICENSE) for multi-license details.
