# Iteration 007: Omnilingual ASR Corpus

## Overview

| Property | Value |
|----------|-------|
| **Date** | 2025-12-25 |
| **Source** | Meta Omnilingual ASR Corpus |
| **Status** | ✅ Completed |

## Results

| Metric | Value |
|--------|-------|
| **Parquet files** | 4 |
| **Total rows** | 443 |
| **Unique texts** | 437 |
| **Characters** | 446,201 |
| **Words** | 60,485 |

## Source

- **HuggingFace**: Sellopale/omnilingualpaleoi
- **Original**: facebook/omnilingual-asr-corpus
- **License**: CC-BY-4.0
- **Language code**: her_Latn (ISO 639-3)

## Content

Spontaneous speech transcriptions:
- Natural conversational Herero
- Includes disfluencies, hesitations
- Various speakers and prompts

## Data Output

- **Location**: `data/raw/omnilingual_hz/2025-12-25/`
- **Combined**: `all_omnilingual.jsonl`
- **Source files**: `source/*.parquet`
