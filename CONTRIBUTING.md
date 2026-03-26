# Contributing to Herero Dataset

Thank you for your interest in contributing to the Herero language dataset!

## Adding New Data Sources

When adding a new data source, follow these steps:

1. **Create source documentation** in `docs/sources/<source_name>.md`
2. **Verify licensing** - ensure the source allows redistribution
3. **Create a scraper** in `scripts/scrapers/<source_name>/`
4. **Create an iteration folder** in `iterations/iteration_XXX_<source_name>/`
5. **Update CHANGELOG.md** with the new source

## Data Quality Standards

- All text must be verified as Herero language
- Minimum 50 characters per document
- No duplicate content across sources
- Proper Unicode handling

## Code Standards

- Python 3.9+
- Use type hints
- Include docstrings
- Follow PEP 8

## Legal Requirements

- All sources must have compatible licenses (CC BY-SA preferred)
- Document attribution in `docs/legal/LICENSE_ATTRIBUTION.md`
- Respect robots.txt and rate limits when scraping
