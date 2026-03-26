# Iteration 001: Wikipedia Herero Scraping

## Overview

| Property | Value |
|----------|-------|
| **Date** | 2025-12-24 |
| **Source** | Wikimedia Incubator Wp/hz |
| **Status** | ✅ Completed |

## Goals

- [x] Scrape all ~102 pages from Herero Wikipedia incubator
- [x] Extract and clean article text
- [x] Store raw and processed data
- [x] Generate statistics

## Results

| Metric | Value |
|--------|-------|
| Pages scraped | 102 |
| Total characters | 48,231 |
| Total words | 6,109 |
| Avg chars/doc | ~473 |

## Data Output

- **Location**: `data/raw/wikipedia_hz/2025-12-24/`
- **Files**: 102 individual JSON files + `all_articles.jsonl`
- **Statistics**: `stats.json`

## Categories Found

- Africa (general)
- Namibia (country, regions)
- Omaheke (region)
- Kunene (region)
- Ovakriste (Christianity)

## Observations

- Article lengths vary significantly (25 to 2000+ chars)
- Some articles are stubs with minimal content
- Good coverage of Herero culture and Namibian geography
- Mix of religious, political, and cultural topics

## Next Steps

1. Process and deduplicate content
2. Identify quality thresholds (min char count)
3. Plan next data source (PDFs, other texts)
