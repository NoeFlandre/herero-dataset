"""
HTML Parser for Wikipedia Herero articles.

Extracts clean text content from Wikipedia HTML pages.
"""

from typing import Optional
from bs4 import BeautifulSoup, NavigableString


def extract_article_text(soup: BeautifulSoup) -> str:
    """
    Extract clean article text from a Wikipedia page.
    
    Removes navigation, templates, infoboxes, and other non-content elements.
    
    Args:
        soup: BeautifulSoup object of the page
    
    Returns:
        Cleaned article text
    """
    # Find the main content div
    content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        return ""
    
    # Find the parser output
    parser_output = content.find('div', class_='mw-parser-output')
    if not parser_output:
        parser_output = content
    
    # Remove unwanted elements
    elements_to_remove = [
        # Navigation and UI
        'script', 'style', 'noscript',
        # Tables (often infoboxes, navboxes)
        'table',
        # Template boxes
        {'class': 'navbox'},
        {'class': 'infobox'},
        {'class': 'sidebar'},
        {'class': 'mbox'},
        {'class': 'ambox'},
        {'class': 'tmbox'},
        {'class': 'ombox'},
        # References
        {'class': 'references'},
        {'class': 'reflist'},
        # Edit links
        {'class': 'mw-editsection'},
        # Table of contents
        {'id': 'toc'},
        {'class': 'toc'},
        # Categories
        {'id': 'catlinks'},
        # Hatnotes
        {'class': 'hatnote'},
        # Stub notices
        {'class': 'stub'},
        # Coordinates
        {'class': 'geo-default'},
        {'id': 'coordinates'},
    ]
    
    for selector in elements_to_remove:
        if isinstance(selector, str):
            for elem in parser_output.find_all(selector):
                elem.decompose()
        elif isinstance(selector, dict):
            for elem in parser_output.find_all(**selector):
                elem.decompose()
    
    # Extract text from paragraphs and headings
    text_parts = []
    
    for elem in parser_output.find_all(['p', 'h2', 'h3', 'h4', 'li']):
        # Skip empty elements
        text = elem.get_text(strip=True)
        if text:
            # Add newlines before headings
            if elem.name in ['h2', 'h3', 'h4']:
                # Remove [edit] suffixes
                text = text.replace('[edit]', '').strip()
                text_parts.append(f"\n{text}\n")
            else:
                text_parts.append(text)
    
    # Join and clean up
    full_text = '\n'.join(text_parts)
    
    # Clean up whitespace
    full_text = clean_text(full_text)
    
    return full_text


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw text
    
    Returns:
        Cleaned text
    """
    import unicodedata
    import re
    
    # Unicode normalization (NFC)
    text = unicodedata.normalize('NFC', text)
    
    # Remove zero-width characters
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text
