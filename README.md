# Herero Language Dataset

[![HuggingFace Dataset](https://img.shields.io/badge/Dataset-HuggingFace-blue)](https://huggingface.co/datasets/NoeFlandre/herero-dataset)

A curated dataset of Herero (Otjiherero) language text for NLP research and language model development.

> **Note:** The data is hosted on [HuggingFace](https://huggingface.co/datasets/NoeFlandre/herero-dataset). This repository contains the code and documentation.

## Dataset Summary

| Metric | Value |
|--------|-------|
| **Total Documents** | 1,951 |
| **Total Words** | 870,941 |
| **Total Characters** | 5,882,568 |
| **Languages** | Herero (hz) |
| **License** | MIT |

## Sources

| Source | Documents | Words | License |
|--------|-----------|-------|---------|
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
| **train** | 1,761 |
| **validation** | 95 |
| **test** | 95 |

## Usage

```python
from datasets import load_dataset

# Load from HuggingFace Hub
dataset = load_dataset("NoeFlandre/herero-dataset")

# Access splits
train_data = dataset["train"]
val_data = dataset["validation"]
test_data = dataset["test"]

# Get all training text
train_texts = [example["text"] for example in train_data]
```

## Structure

```
herero_dataset/
├── huggingface_dataset/        # HuggingFace-ready dataset (uploaded to HF)
│   ├── README.md               # Dataset card
│   ├── LICENSE                # MIT license
│   └── data/
│       ├── train.parquet
│       ├── validation.parquet
│       └── test.parquet
├── scripts/                    # Data collection and processing
│   ├── create_hf_dataset.py   # Main dataset creation script
│   ├── scrapers/              # Source-specific scrapers
│   └── processing/            # Data curation scripts
├── tests/                     # TDD tests
├── docs/                      # Documentation
├── Dockerfile                 # Container definition
├── pyproject.toml            # Project configuration (uv-compatible)
├── CITATION.cff               # Citation file
└── README.md
```

## Quick Start

### Using Docker

```bash
docker build -t herero-dataset .
docker run herero-dataset
```

### Using uv

```bash
uv sync
uv run pytest tests/ -v
```

### Using pip

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Running Tests

```bash
pytest tests/ -v
```

## License

MIT License - See [LICENSE](LICENSE)
