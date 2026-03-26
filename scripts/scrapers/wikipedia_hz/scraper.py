"""
Wikipedia Herero (Wp/hz) Scraper

Scrapes all articles from the Herero Wikipedia Incubator.
"""

import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup

from .config import (
    BASE_URL,
    API_URL,
    PREFIX_INDEX_URL,
    USER_AGENT,
    RATE_LIMIT_SECONDS,
    MAX_RETRIES,
    TIMEOUT_SECONDS,
    EXCLUDED_PREFIXES,
    OUTPUT_DIR,
    DATE_FORMAT,
)
from .parser import extract_article_text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_session() -> requests.Session:
    """Create a requests session with proper headers."""
    session = requests.Session()
    session.headers.update({
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    return session


def get_page_urls(session: Optional[requests.Session] = None) -> List[str]:
    """
    Fetch all article URLs from the Herero Wikipedia incubator.
    
    Uses the Special:PrefixIndex page to get a list of all Wp/hz/ pages.
    
    Returns:
        List of article URLs
    """
    if session is None:
        session = get_session()
    
    logger.info("Fetching page list from PrefixIndex...")
    
    try:
        response = session.get(PREFIX_INDEX_URL, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch page list: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all links that start with /wiki/Wp/hz/
    urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/Wp/hz/'):
            # Skip excluded prefixes
            full_url = BASE_URL + href
            page_title = href.replace('/wiki/', '')
            
            if not any(page_title.startswith(exc) for exc in EXCLUDED_PREFIXES):
                urls.append(full_url)
    
    # Remove duplicates while preserving order
    urls = list(dict.fromkeys(urls))
    
    logger.info(f"Found {len(urls)} article URLs")
    return urls


def scrape_page(url: str, session: requests.Session) -> Optional[Dict]:
    """
    Scrape a single Wikipedia page.
    
    Args:
        url: Full URL of the page to scrape
        session: Requests session
    
    Returns:
        Dictionary with page data or None if failed
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1', {'id': 'firstHeading'})
            title = title_elem.get_text(strip=True) if title_elem else url.split('/')[-1]
            
            # Clean title (remove Wp/hz/ prefix)
            if title.startswith('Wp/hz/'):
                title = title[6:]
            
            # Extract article text
            text = extract_article_text(soup)
            
            # Extract categories
            categories = []
            for cat_link in soup.select('#mw-normal-catlinks ul li a'):
                cat_name = cat_link.get_text(strip=True)
                if cat_name.startswith('Wp/hz/'):
                    cat_name = cat_name[6:]
                categories.append(cat_name)
            
            return {
                'source_url': url,
                'title': title,
                'text': text,
                'categories': categories,
                'scraped_at': datetime.utcnow().isoformat() + 'Z',
                'word_count': len(text.split()),
                'char_count': len(text),
            }
            
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for {url}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RATE_LIMIT_SECONDS * 2)
    
    logger.error(f"Failed to scrape {url} after {MAX_RETRIES} attempts")
    return None


def run_scraper(output_dir: Optional[str] = None) -> List[Dict]:
    """
    Run the full scraping pipeline.
    
    Args:
        output_dir: Directory to save raw data (uses config default if None)
    
    Returns:
        List of scraped documents
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    # Create dated output directory
    date_str = datetime.now().strftime(DATE_FORMAT)
    output_path = Path(output_dir) / date_str
    output_path.mkdir(parents=True, exist_ok=True)
    
    session = get_session()
    
    # Get all page URLs
    urls = get_page_urls(session)
    
    if not urls:
        logger.error("No URLs found to scrape")
        return []
    
    # Scrape each page
    documents = []
    for i, url in enumerate(urls):
        logger.info(f"Scraping [{i+1}/{len(urls)}]: {url}")
        
        doc = scrape_page(url, session)
        if doc:
            # Add ID
            doc['id'] = f"wp_hz_{i+1:03d}"
            doc['source'] = 'wikipedia_incubator'
            doc['language'] = 'hz'
            doc['license'] = 'CC-BY-SA-3.0'
            
            documents.append(doc)
            
            # Save individual file
            page_filename = url.split('/')[-1].replace(':', '_') + '.json'
            with open(output_path / page_filename, 'w', encoding='utf-8') as f:
                json.dump(doc, f, ensure_ascii=False, indent=2)
        
        # Rate limiting
        if i < len(urls) - 1:
            time.sleep(RATE_LIMIT_SECONDS)
    
    # Save combined JSONL
    jsonl_path = output_path / 'all_articles.jsonl'
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    logger.info(f"Scraped {len(documents)} documents to {output_path}")
    
    # Save statistics
    stats = {
        'scrape_date': date_str,
        'total_urls': len(urls),
        'successful_scrapes': len(documents),
        'total_characters': sum(d['char_count'] for d in documents),
        'total_words': sum(d['word_count'] for d in documents),
    }
    with open(output_path / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    return documents


if __name__ == '__main__':
    run_scraper()
