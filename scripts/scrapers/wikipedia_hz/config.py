"""Wikipedia Herero (Wp/hz) Scraper Configuration"""

# Base URLs
BASE_URL = "https://incubator.wikimedia.org"
API_URL = f"{BASE_URL}/w/api.php"
PREFIX_INDEX_URL = f"{BASE_URL}/wiki/Special:PrefixIndex/Wp/hz/"

# Scraping settings
USER_AGENT = "HereroDatasetBot/1.0 (Research project for Herero language LLM; github.com/your-repo)"
RATE_LIMIT_SECONDS = 2.0  # Delay between requests (respectful crawling)
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Content filtering
EXCLUDED_PREFIXES = [
    "Wp/hz/Talk:",
    "Wp/hz/User:",
    "Template:Wp/hz/",
    "Category:Wp/hz",
]

# Output settings
OUTPUT_DIR = "data/raw/wikipedia_hz"
DATE_FORMAT = "%Y-%m-%d"
