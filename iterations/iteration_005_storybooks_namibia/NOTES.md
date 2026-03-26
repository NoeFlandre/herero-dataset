# Iteration 005: Storybooks Namibia

## Overview

| Property | Value |
|----------|-------|
| **Date** | 2025-12-25 |
| **Source** | Storybooks Namibia |
| **Status** | ✅ Completed |

## Results

| Metric | Value |
|--------|-------|
| **Stories** | 46 |
| **Characters** | 83,476 |
| **Words** | 13,246 |

## Extraction Method

Website uses bilingual display with CSS classes:
- **`class="def"`** = Herero text (extracted)
- **`class="l1"`** = English text (excluded)

Scraper selects only elements with class `def` to get pure Herero.

## Notable Stories

| Story | Chars | Description |
|-------|-------|-------------|
| Ozosewa wina ze hepa orusuvero | 11,391 | Longest story |
| Simbegwire | 5,243 | Traditional tale |
| Magozwe | 5,072 | Contemporary |

## Data Output

- **Location**: `data/raw/storybooks_namibia/2025-12-25/`
- **Combined**: `all_storybooks.jsonl`
- **Individual**: 46 story JSON files

## Legal Verification ✅

- CC BY 3.0/4.0 open license
- African Storybook allows repurposing
- Attribution to original authors included
