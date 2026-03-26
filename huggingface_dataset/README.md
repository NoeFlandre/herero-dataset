---
license: other
license_name: multiple-licenses
pretty_name: Herero Language Dataset
language:
- hz
task_categories:
- text-classification
---

# Herero Language Dataset

A **multi-license collection** of [Herero (Otjiherero)](https://en.wikipedia.org/wiki/Herero_language) text for NLP research. This is **not** a derivative work—sources are aggregated with original licenses preserved.

**⚠️ WARNING: This repository is a redistribution of materials from multiple upstream sources under different licenses. Each example remains subject to its original source license. Users are responsible for checking per-row licensing before reuse.**

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

| Split | Documents | % |
|-------|-----------|---|
| train | 1,761 | 90% |
| validation | 95 | 5% |
| test | 95 | 5% |

## Schema

Each row includes provenance columns:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique document ID |
| `text` | string | Herero text (NFC normalized) |
| `source` | string | Data source name |
| `original_license` | string | Source license (check this!) |
| `original_url` | string | Link to original source |
| `changes_made` | string | Transformations applied |
| `license_type` | string | License category |
| `url` | string | Source URL |
| `word_count` | int | Word count |
| `char_count` | int | Character count |

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("NoeFlandre/herero-dataset")

# Check per-row license BEFORE use
for example in dataset["train"]:
    print(f"License: {example['original_license']} - {example['source']}")
```

## Collection Classification

This dataset is a **collection**, not an adaptation:
- Text is aggregated from sources without material modification
- Original text is preserved (only formatting normalized)
- No translation, rewriting, or merging across sources
- Source boundaries maintained via `source` column

## Quality Assurance

- **Deduplication**: Within-source SHA-256 content hashing
- **Normalization**: Unicode NFC normalization (no text rewriting)
- **Filtering**: Min-length 50 chars
- **Reproducibility**: Fixed random seed (42)

## Known Limitations

- ~871K words is moderate for low-resource language research
- FineWeb-2 dominates (~77% of content)
- Historical text uses 19th-century orthography
- Speech transcripts may contain disfluencies

## Ethical Considerations

- No personal data included
- All content publicly available at time of scraping
- Attribution preserved via `original_url` column
- Users must respect individual source licenses

## Licensing Summary

| License Type | Sources | Requirements |
|-------------|---------|--------------|
| Public Domain | 1 | None |
| CC BY | 3 | Attribution |
| CC BY-SA | 1 | Attribution + ShareAlike |
| ODC-By | 2 | Attribution + Keep open |

**You must check the `original_license` column for each example.**

## Files

- `data/train.parquet` - Training split
- `data/validation.parquet` - Validation split
- `data/test.parquet` - Test split
- `sources.csv` - Full source manifest

## Disclaimer

This documentation is provided for informational purposes only and does not constitute legal advice. Uncertain licensing cases were reviewed conservatively. For legal questions, consult the original license texts or seek professional counsel.
