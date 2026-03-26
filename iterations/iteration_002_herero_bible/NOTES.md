# Iteration 002: Herero Bible (1849)

## Overview

| Property | Value |
|----------|-------|
| **Date** | 2025-12-24 |
| **Source** | Archive.org - Herero Bible OCR |
| **Status** | ✅ Completed |

## Source Details

- **Title**: Omahungi Oa Embo Ra Jehova Na Omaimpuriro Mo Otjiherero
- **Year**: 1849 (Public Domain)
- **Publisher**: Rhenish Missionary Society
- **URL**: https://archive.org/stream/OmahungiOaEmboRaJehovaNaOmaimpurir/

## Results

| Metric | Value |
|--------|-------|
| **Total sections** | 81 |
| **Stories (EHUNGI)** | 47 |
| **Hymns (OMAIMPURIRO)** | 34 |
| **Characters** | 154,587 |
| **Words** | 26,807 |
| **Avg chars/section** | 1,908 |

## Data Output

- **Location**: `data/raw/herero_bible/2025-12-24/`
- **Combined**: `all_bible.jsonl` (196KB)
- **Individual**: 81 JSON files (stories + hymns)
- **Cleaned text**: `herero_bible_cleaned.txt`

## Cleaning Applied

- ✅ Removed "Digitized by Google" markers
- ✅ Removed standalone page numbers
- ✅ Removed single-letter OCR artifacts
- ✅ Removed musical notation markers
- ✅ Normalized whitespace

## Historical Significance

This 1849 publication is one of the earliest substantial written works in Otjiherero, providing invaluable linguistic data for the language's 19th-century form.

## Next Steps

1. Combine with Wikipedia data for v1.0 dataset
2. Consider additional historical sources (PDFs)
