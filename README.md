# Otjiherero Language Dataset

A curated dataset of text in the **Otjiherero (Herero)** language for NLP research and language model development.

## Dataset Versions

| Version | Documents | Characters | License |
|---------|-----------|------------|---------|
| **HuggingFace** | 651 | 1.14M | CC BY-SA 4.0 |
| **Local** | 667 | 1.60M | Personal use |

## Sources (HuggingFace Version)

| Source | Documents | License |
|--------|-----------|---------|
| Wikipedia Incubator (Wp/hz) | 102 | CC BY-SA 3.0 |
| Herero Bible (1849) | 81 | Public Domain |
| Storybooks Namibia | 46 | CC BY 3.0/4.0 |
| Omnilingual ASR Corpus | 437 | CC BY 4.0 |
| GlotCC-V1 | 20 | CC BY 4.0 |

## Structure

```
herero_dataset/
├── data/
│   ├── raw/                    # Original scraped data
│   └── processed/
│       ├── huggingface/        # ✅ Safe for publication
│       │   ├── herero_pretraining_curated.jsonl
│       │   └── curation_stats.json
│       └── local/              # 🏠 Personal use only
│           ├── herero_pretraining_curated.jsonl
│           └── curation_stats.json
├── docs/
│   ├── legal/                  # License verification
│   └── sources/                # Source documentation
├── iterations/                 # Processing logs
└── scripts/
    ├── scrapers/               # Data collection scripts
    └── processing/             # Dataset curation scripts
```

## Usage

```python
from datasets import load_dataset

# Load from file
dataset = load_dataset('json', data_files='data/processed/huggingface/herero_pretraining_curated.jsonl')
```

## License

CC BY-SA 4.0 - See [LICENSE](LICENSE)

## Attribution

See [docs/legal/LICENSE_ATTRIBUTION.md](docs/legal/LICENSE_ATTRIBUTION.md) for full attribution.