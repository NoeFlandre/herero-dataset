---
annotations_creators:
- no-annotation
language:
- hz
language_creators:
- found
license: mit
multilinguality:
- monolingual
pretty_name: Herero Language Dataset
size_categories:
- 1K<n<10K
source_datasets:
- original
tags:
- herero
- otjiherero
- namibia
- bantu
- low-resource
- african-languages
- pretraining
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
---

# Herero Language Dataset

[![GitHub Repository](https://img.shields.io/badge/Code-GitHub-blue)](https://github.com/NoeFlandre/herero-dataset)

A curated dataset of [Herero (Otjiherero)](https://en.wikipedia.org/wiki/Herero_language) language text for LLM pretraining and NLP research. Herero is a Bantu language spoken by ~250,000 people in Namibia and Botswana.

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

| Split | Documents | % |
|-------|-----------|---|
| train | 1,761 | 90% |
| validation | 95 | 5% |
| test | 95 | 5% |

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique document ID (source_prefix + number) |
| `text` | string | Herero text (NFC normalized) |
| `source` | string | Data source name |
| `url` | string | Original source URL |
| `license` | string | Source license |
| `word_count` | int | Word count |
| `char_count` | int | Character count |

Splits are stratified by source to ensure representation in all splits.

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("NoeFlandre/herero-dataset")

train_data = dataset["train"]
val_data = dataset["validation"]
test_data = dataset["test"]
```

## Quality Assurance

- **Deduplication**: SHA-256 content hashing
- **Normalization**: Unicode NFC normalization
- **Filtering**: Minimum 50-character threshold
- **Reproducibility**: Fixed random seed (42)

## Known Limitations

- ~871K words is moderate for low-resource language research
- FineWeb-2 dominates (~77% of content)
- Historical text uses 19th-century orthography
- Speech transcripts may contain disfluencies

## Licensing

Dataset: MIT

Source content retains original licenses. See the [GitHub repository](https://github.com/NoeFlandre/herero-dataset) for full attribution.

## Citation

```bibtex
@dataset{herero_dataset,
  title = {Herero Language Dataset},
  author = {Noé Flandre},
  year = {2026},
  url = {https://huggingface.co/datasets/NoeFlandre/herero-dataset}
}
```

## Acknowledgments

- Wikimedia Foundation (Wikipedia Incubator)
- Meta AI Research (Omnilingual ASR)
- CIS LMU Munich (GlotCC)
- HuggingFace (FineWeb-2, FinePDFs)
- African Storybook / Saide
- Rhenish Missionary Society
