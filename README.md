# Herero Language Dataset

[![HuggingFace Dataset](https://img.shields.io/badge/Dataset-HuggingFace-blue)](https://huggingface.co/datasets/NoeFlandre/herero-dataset)

A curated [Herero (Otjiherero)](https://en.wikipedia.org/wiki/Herero_language) language dataset for NLP research and LLM pretraining.

**1,951 documents · 871K words · 7 sources · MIT License**

## Quick Start

```python
from datasets import load_dataset
dataset = load_dataset("NoeFlandre/herero-dataset")
```

## Dataset Summary

| Metric | Value |
|--------|-------|
| Documents | 1,951 |
| Words | 870,941 |
| Characters | 5,882,568 |
| Language | Herero (hz) |
| License | MIT |

## Sources

| Source | Docs | Words | License |
|--------|-----:|------:|---------|
| FineWeb-2 | 1,272 | 672,378 | ODC-By 1.0 |
| Omnilingual ASR | 437 | 60,485 | CC BY 4.0 |
| GlotCC-V1 | 20 | 75,982 | CC BY 4.0 |
| Herero Bible (1849) | 81 | 26,807 | Public Domain |
| Storybooks Namibia | 46 | 13,246 | CC BY 3.0/4.0 |
| FinePDFs | 25 | 17,800 | ODC-By 1.0 |
| Wikipedia Incubator | 70 | 4,243 | CC BY-SA 3.0 |

## Data Splits

| Split | Documents |
|-------|-----------|
| train | 1,761 |
| validation | 95 |
| test | 95 |

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique document ID |
| `text` | string | Herero text (NFC normalized) |
| `source` | string | Data source name |
| `url` | string | Original source URL |
| `license` | string | Source license |
| `word_count` | int | Word count |
| `char_count` | int | Character count |

## Installation

```bash
# Using uv (recommended)
uv sync

# Using pip
pip install -r requirements.txt
```

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
├── huggingface_dataset/   # Dataset on HF Hub
│   └── data/
│       ├── train.parquet
│       ├── validation.parquet
│       └── test.parquet
├── scripts/              # Scrapers & processing
├── tests/                # TDD tests
├── docs/                 # Source documentation
├── Dockerfile
├── pyproject.toml
└── README.md
```

## License

MIT License - See [LICENSE](LICENSE)
