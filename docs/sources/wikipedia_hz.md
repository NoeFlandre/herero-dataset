# Wikipedia Incubator - Herero (Wp/hz)

## Source Information

| Property | Value |
|----------|-------|
| **URL** | https://incubator.wikimedia.org/wiki/Wp/hz |
| **Language Code** | ISO 639-1: `hz`, ISO 639-3: `her` |
| **License** | CC BY-SA 3.0 |
| **Estimated Pages** | ~102 |
| **Categories** | 15 subcategories |

## Content Overview

The Herero Wikipedia Incubator contains articles primarily about:

- **Namibia** (~10 pages) - Country, regions, cities
- **Africa** (~10 pages) - Continent, countries
- **Omaheke** (~7 pages) - Namibian region
- **Kunene** (~3 pages) - Namibian region  
- **Religion** (~4 pages) - Ongamburiro (traditional beliefs)

## Scraping Approach

### Entry Points

1. **All pages list**: `Special:PrefixIndex/Wp/hz/`
2. **Main category**: `Category:Wp/hz`

### Rate Limiting

- 2 seconds between requests
- User-Agent: `HereroDatasetBot/1.0 (Research)`

### Exclusions

- Redirect pages
- Template pages (`Template:Wp/hz/`)
- Category pages
- Discussion pages

## Known Issues

- Some articles are stubs with minimal content
- Template text may appear in some articles
- Most activity was around 2016 (project is relatively static)
