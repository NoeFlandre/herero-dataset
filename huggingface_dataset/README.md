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

# Herero Language Dataset (Otjiherero)

[![GitHub Repository](https://img.shields.io/badge/Code-GitHub-blue)](https://github.com/NoeFlandre/herero-dataset)

A curated dataset of Herero (Otjiherero) language text for LLM pretraining and NLP research. This dataset contains **1,951 documents** with approximately **871,000 words** (5.9 million characters) from 7 curated sources. Herero is a Bantu language spoken by ~250,000 people in Namibia and Botswana.

> **Note:** The data is hosted here on HuggingFace. For code, scripts, and documentation, see the [GitHub repository](https://github.com/NoeFlandre/herero-dataset).

## Dataset Summary

| Metric | Value |
|--------|-------|
| **Total Documents** | 1,951 |
| **Total Words** | 870,941 |
| **Total Characters** | 5,882,568 |
| **Languages** | Herero (hz) |
| **License** | MIT |

## Dataset Statistics by Source

| Source | Documents | Words | License |
|--------|-----------|-------|---------|
| FineWeb-2 | 1,272 | 672,378 | ODC-By 1.0 |
| Omnilingual ASR | 437 | 60,485 | CC BY 4.0 |
| GlotCC-V1 | 20 | 75,982 | CC BY 4.0 |
| Herero Bible (1849) | 81 | 26,807 | Public Domain |
| Storybooks Namibia | 46 | 13,246 | CC BY 3.0/4.0 |
| FinePDFs | 25 | 17,800 | ODC-By 1.0 |
| Wikipedia Incubator | 70 | 4,243 | CC BY-SA 3.0 |
| **Total** | **1,951** | **870,941** | |

## Data Splits

| Split | Documents | Percentage |
|-------|-----------|------------|
| **train** | 1,761 | 90% |
| **validation** | 95 | 5% |
| **test** | 95 | 5% |

## Dataset Structure

### Data Format

JSONL files with the following schema:

```json
{
  "id": "fw2_00001",
  "text": "Herero language text content...",
  "source": "fineweb2",
  "url": "https://example.com/source",
  "license": "ODC-By 1.0",
  "word_count": 123,
  "char_count": 789
}
```

### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique document identifier (source prefix + number) |
| `text` | string | The Herero language text content (NFC normalized) |
| `source` | string | Name of the data source |
| `url` | string | Original source URL |
| `license` | string | License of the source content |
| `word_count` | int | Number of words in the text |
| `char_count` | int | Number of characters in the text |

### Data Splits

| Split | Purpose | Documents |
|-------|---------|-----------|
| `train` | Model training | 1,761 (90%) |
| `validation` | Hyperparameter tuning | 95 (5%) |
| `test` | Final evaluation | 95 (5%) |

Splits are stratified by source to ensure each source is represented in all splits.

## Usage

### Loading the Dataset

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

### For LLM Continual Pretraining

```python
from datasets import load_dataset

dataset = load_dataset("NoeFlandre/herero-dataset")

# Combine all training text
def get_training_corpus():
    for example in dataset["train"]:
        yield example["text"]

# Use with your tokenizer
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("your-base-model")

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=2048)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
```

## Dataset Creation

### Curation Rationale

Herero is a low-resource language with limited digital resources. This dataset was curated to:
1. Enable development of Herero language models
2. Support NLP research on low-resource African languages
3. Provide standardized train/val/test splits for reproducible research

### Quality Assurance

- **Deduplication**: SHA-256 content hashing
- **Normalization**: Unicode NFC normalization applied
- **Filtering**: Minimum 50-character threshold
- **Stratification**: All sources represented in all splits
- **Reproducibility**: Fixed random seed (42) for deterministic splits

### Source Data

| Source | URL | Description |
|--------|-----|-------------|
| Wikipedia Incubator | [Wp/hz](https://incubator.wikimedia.org/wiki/Wp/hz) | Encyclopedia articles |
| Herero Bible (1849) | [Archive.org](https://archive.org) | Historical religious text |
| Storybooks Namibia | [storybooksnamibia.net](https://storybooksnamibia.net) | Children's stories |
| Omnilingual ASR | [HuggingFace](https://huggingface.co/datasets/facebook/omnilingual-asr-corpus) | Speech transcriptions |
| GlotCC-V1 | [HuggingFace](https://huggingface.co/datasets/cis-lmu/GlotCC-V1) | Web-scraped text |
| FineWeb-2 | [HuggingFace](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | High-quality web text |
| FinePDFs | [HuggingFace](https://huggingface.co/datasets/HuggingFaceFW/finepdfs) | PDF-extracted text |

## Considerations

### Intended Uses

- LLM pretraining/fine-tuning for Herero
- Language modeling research
- Low-resource NLP research
- Linguistic analysis

### Limitations

- Moderate corpus size (~871K words) compared to high-resource languages
- Domain imbalance (web content overrepresented via FineWeb-2)
- Historical text (1849) uses archaic orthography
- Speech transcriptions may include disfluencies

### Bias Considerations

- Geographic bias toward Namibia
- Historical texts reflect 19th-century perspectives
- Web content reflects online author demographics

## Licensing

**Dataset License**: MIT

This dataset is released under MIT license. Source content retains their original licenses:

| Source | License |
|--------|---------|
| FineWeb-2 | ODC-By 1.0 |
| FinePDFs | ODC-By 1.0 |
| Omnilingual ASR | CC BY 4.0 |
| GlotCC-V1 | CC BY 4.0 |
| Storybooks Namibia | CC BY 3.0/4.0 |
| Wikipedia Incubator | CC BY-SA 3.0 |
| Herero Bible (1849) | Public Domain |

## Citation

```bibtex
@dataset{herero_dataset,
  title = {Herero Language Dataset (Otjiherero)},
  author = {Noé Flandre},
  year = {2026},
  publisher = {HuggingFace},
  url = {https://huggingface.co/datasets/NoeFlandre/herero-dataset}
}
```

## Acknowledgments

- Wikimedia Foundation and Wikipedia Incubator contributors
- Meta AI Research (Omnilingual ASR)
- CIS LMU Munich (GlotCC)
- HuggingFace (FineWeb-2, FinePDFs)
- African Storybook / Saide (Storybooks Namibia)
- Rhenish Missionary Society (historical Bible text)
