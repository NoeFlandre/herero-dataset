---
annotations_creators:
- no-annotation
language:
- hz
language_creators:
- found
license: cc-by-sa-4.0
multilinguality:
- monolingual
pretty_name: Herero Language Corpus
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

# Herero Language Corpus (Otjiherero)

A research-grade dataset of Herero (Otjiherero) language text for LLM pretraining and NLP research.

## Dataset Description

- **Homepage**: [GitHub Repository](https://github.com/your-username/herero-corpus)
- **Languages**: Herero (hz/her)
- **License**: CC BY-SA 4.0

### Summary

This dataset contains **1,951 documents** with approximately **871,000 words** (5.9 million characters) of Herero language text from 7 curated sources. Herero (Otjiherero) is a Bantu language spoken by ~250,000 people in Namibia and Botswana.

**Key Features:**
- ✅ Train/validation/test splits for proper ML evaluation
- ✅ Stratified sampling ensuring source diversity in all splits
- ✅ Deduplicated using SHA-256 content hashing
- ✅ Unicode normalized (NFC)
- ✅ All sources verified for open licensing
- ✅ Reproducible (random seed: 42)

## Dataset Statistics

| Split | Documents | Words | Characters |
|-------|-----------|-------|------------|
| **train** | 1,761 | 781,598 | 5,276,082 |
| **validation** | 95 | 48,703 | 329,112 |
| **test** | 95 | 40,640 | 277,374 |
| **Total** | 1,951 | 870,941 | 5,882,568 |

### By Source

| Source | Docs | Words | License |
|--------|------|-------|---------|
| FineWeb-2 | 1,272 | 672,378 | ODC-By 1.0 |
| GlotCC-V1 | 20 | 75,982 | CC BY 4.0 |
| Omnilingual ASR | 437 | 60,485 | CC BY 4.0 |
| Herero Bible (1849) | 81 | 26,807 | Public Domain |
| FinePDFs | 25 | 17,800 | ODC-By 1.0 |
| Storybooks Namibia | 46 | 13,246 | CC BY 3.0/4.0 |
| Wikipedia Incubator | 70 | 4,243 | CC BY-SA 3.0 |

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
dataset = load_dataset("your-username/herero-corpus")

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

dataset = load_dataset("your-username/herero-corpus")

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

### Evaluation Example

```python
# Perplexity evaluation on test set
from evaluate import load
perplexity = load("perplexity", module_type="metric")

test_texts = [ex["text"] for ex in dataset["test"]]
results = perplexity.compute(predictions=test_texts, model_id="your-model")
```

## Dataset Creation

### Curation Rationale

Herero is a low-resource language with limited digital resources. This dataset was curated to:
1. Enable development of Herero language models
2. Support NLP research on low-resource African languages
3. Provide standardized train/val/test splits for reproducible research

### Quality Assurance

- **Deduplication**: SHA-256 content hashing (17 duplicates removed)
- **Normalization**: Unicode NFC normalization applied
- **Filtering**: Minimum 50-character threshold (15 documents filtered)
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

✅ **Recommended:**
- LLM pretraining/fine-tuning for Herero
- Language modeling research
- Low-resource NLP research
- Linguistic analysis

⚠️ **Use with caution:**
- Machine translation (limited parallel data)
- Sentiment analysis (no annotations)

### Limitations

- Moderate corpus size (~871K words) compared to high-resource languages
- Domain imbalance (religious content overrepresented)
- Historical text (1849) uses archaic orthography
- Speech transcriptions may include disfluencies

### Bias Considerations

- Religious/spiritual content overrepresented
- Geographic bias toward Namibia
- Historical texts reflect 19th-century perspectives
- Web content reflects online author demographics

### Personal/Sensitive Information

- ❌ No personal identifying information
- ❌ No private communications
- ✅ Only publicly available content

## Licensing

**Dataset License**: CC BY-SA 4.0

All sources are compatible with CC BY-SA 4.0:

| Source | License | Compatible |
|--------|---------|------------|
| Wikipedia Incubator | CC BY-SA 3.0 | ✅ |
| Herero Bible | Public Domain | ✅ |
| Storybooks Namibia | CC BY 3.0/4.0 | ✅ |
| Omnilingual ASR | CC BY 4.0 | ✅ |
| GlotCC-V1 | CC BY 4.0 | ✅ |
| FineWeb-2 | ODC-By 1.0 | ✅ |
| FinePDFs | ODC-By 1.0 | ✅ |

## Citation

```bibtex
@dataset{herero_corpus_2024,
  title = {Herero Language Corpus (Otjiherero)},
  author = {Your Name},
  year = {2024},
  publisher = {HuggingFace},
  url = {https://huggingface.co/datasets/your-username/herero-corpus},
  note = {A research-grade dataset of Herero language text for LLM pretraining}
}
```

## Acknowledgments

- Wikimedia Foundation and Wikipedia Incubator contributors
- African Storybook / Saide and Storybooks Namibia
- Meta AI Research (Omnilingual ASR)
- CIS LMU Munich (GlotCC)
- HuggingFace (FineWeb-2, FinePDFs)
- Rhenish Missionary Society (historical Bible text)
