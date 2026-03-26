# Herero Language Dataset - Data Card

## Dataset Description

### Summary

A curated dataset of Herero (Otjiherero) language text for LLM pretraining and NLP research. The Herero language is a Bantu language spoken primarily in Namibia and Botswana.

### Languages

- **Primary**: Herero / Otjiherero (`hz` / `her`)

### Dataset Sources

| Source | URL | License | Status |
|--------|-----|---------|--------|
| Wikipedia Incubator | [Wp/hz](https://incubator.wikimedia.org/wiki/Wp/hz) | CC BY-SA 3.0 | ✅ Included |
| Herero Bible (1849) | [Archive.org](https://archive.org/stream/OmahungiOaEmboRaJehovaNaOmaimpurir/) | Public Domain | ✅ Included |
| Storybooks Namibia | [storybooksnamibia.net](https://storybooksnamibia.net/stories/hz/) | CC BY 3.0/4.0 | ✅ Included |
| Omnilingual ASR | [HuggingFace](https://huggingface.co/datasets/Sellopale/omnilingualpaleoi) | CC BY 4.0 | ✅ Included |
| GlotCC-V1 | [HuggingFace](https://huggingface.co/datasets/cis-lmu/GlotCC-V1) | CC BY 4.0 | ✅ Included |
| FineWeb-2 | [HuggingFace](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | ODC-By 1.0 | ✅ Included |
| FinePDFs | [HuggingFace](https://huggingface.co/datasets/HuggingFaceFW/finepdfs) | ODC-By 1.0 | ✅ Included |

## Dataset Structure

### Data Format

JSONL files with the following schema:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique document identifier |
| `source` | string | Data source name |
| `source_url` | string | Original URL |
| `title` | string | Document title |
| `text` | string | Cleaned text content |
| `language` | string | ISO 639-1 code (`hz`) |
| `license` | string | Source license |
| `scraped_at` | string | ISO 8601 timestamp |
| `categories` | array | Topic categories |
| `word_count` | int | Word count |
| `char_count` | int | Character count |

## Dataset Creation

### Collection Process

1. **Wikipedia Incubator**: Automated scraping via MediaWiki API with rate limiting
2. **Text Extraction**: BeautifulSoup parsing, removal of templates/navigation
3. **Deduplication**: Hash-based duplicate detection
4. **Validation**: Language verification, minimum length checks

### Preprocessing

- HTML tag removal
- Unicode normalization (NFC)
- Whitespace normalization
- Template/boilerplate removal

## Considerations

### Intended Uses

- LLM pretraining for Herero language
- NLP research on low-resource Bantu languages
- Linguistic analysis

### Limitations

- Small corpus size for low-resource language
- Potential bias toward topics covered in sources
- May contain some non-Herero text (headers, templates)

### Licensing

This dataset is released under CC BY-SA 4.0. See [LICENSE_ATTRIBUTION.md](legal/LICENSE_ATTRIBUTION.md) for source-specific attributions.
