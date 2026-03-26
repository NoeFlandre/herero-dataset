"""Wikipedia Herero (Wp/hz) Scraper Package"""

from .scraper import run_scraper, get_page_urls, scrape_page
from .parser import extract_article_text, clean_text
from .config import BASE_URL, USER_AGENT, RATE_LIMIT_SECONDS

__all__ = [
    'run_scraper',
    'get_page_urls', 
    'scrape_page',
    'extract_article_text',
    'clean_text',
    'BASE_URL',
    'USER_AGENT',
    'RATE_LIMIT_SECONDS',
]
