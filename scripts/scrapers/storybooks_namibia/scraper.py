"""
Storybooks Namibia Scraper

Scrapes Herero stories from https://storybooksnamibia.net/stories/hz/
Uses CSS class 'def' to extract only Herero text (class 'l1' = English).
"""

import json
import re
import time
from pathlib import Path
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup


# Source metadata
BASE_URL = "https://storybooksnamibia.net"
STORIES_URL = f"{BASE_URL}/stories/hz/"
SOURCE_PUBLISHER = "Storybooks Namibia / African Storybook"
LICENSE = "Creative Commons Attribution 3.0/4.0"
USER_AGENT = "HereroDatasetBot/1.0 (Research project for Herero language LLM)"
RATE_LIMIT = 1.5  # seconds between requests


def get_story_urls() -> list:
    """Get all story URLs from the main page."""
    
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(STORIES_URL, headers=headers)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Find all story links (btn-link class or /stories/hz/XXXX/ pattern)
    story_urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if re.match(r'/stories/hz/\d{4}/?$', href):
            full_url = BASE_URL + href
            if full_url not in story_urls:
                story_urls.append(full_url)
    
    return sorted(story_urls)


def scrape_story(url: str, session: requests.Session) -> dict:
    """Scrape a single story page, extracting only Herero text (class='def')."""
    
    headers = {"User-Agent": USER_AGENT}
    resp = session.get(url, headers=headers)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Extract story ID from URL
    match = re.search(r'/(\d{4})/?$', url)
    story_id = match.group(1) if match else "unknown"
    
    # Get Herero title (h1 with class 'def' or span with class 'def')
    herero_title = ""
    h1 = soup.find('h1')
    if h1:
        def_span = h1.find(class_='def')
        if def_span:
            herero_title = def_span.get_text(strip=True)
        else:
            # Fallback: get first part before English
            full_title = h1.get_text(strip=True)
            herero_title = full_title.split('  ')[0] if '  ' in full_title else full_title
    
    # Get all Herero text elements (class='def')
    herero_paragraphs = []
    
    # Find all elements with class 'def' (Herero content)
    for elem in soup.find_all(class_='def'):
        # Get h3 within def elements (story sentences)
        h3 = elem.find('h3')
        if h3:
            text = h3.get_text(strip=True)
            if text and text not in herero_paragraphs:
                herero_paragraphs.append(text)
        else:
            # Get direct text
            text = elem.get_text(strip=True)
            if text and len(text) > 5 and text not in herero_paragraphs:
                # Skip navigation/metadata text
                if not any(skip in text.lower() for skip in ['level', 'otjiherero', 'written by', 'illustrated', 'translated', 'read by', 'source:', 'storybook']):
                    herero_paragraphs.append(text)
    
    # Get metadata
    author = ""
    translator = ""
    
    for h5 in soup.find_all('h5'):
        text = h5.get_text(strip=True)
        if 'Written by' in text:
            author = text.replace('Written by:', '').replace('Written by', '').strip()
        if 'Translated by' in text:
            translator = text.replace('Translated by:', '').replace('Translated by', '').strip()
    
    # Combine paragraphs
    full_text = "\n\n".join(herero_paragraphs)
    
    return {
        "story_id": story_id,
        "url": url,
        "title": herero_title,
        "text": full_text,
        "paragraphs": len(herero_paragraphs),
        "author": author,
        "translator": translator,
    }


def process_all_stories(output_dir: str) -> dict:
    """Scrape all stories and save to output directory."""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    session = requests.Session()
    
    # Get all story URLs
    print("Fetching story list...")
    story_urls = get_story_urls()
    print(f"Found {len(story_urls)} stories\n")
    
    all_documents = []
    total_chars = 0
    total_words = 0
    
    for i, url in enumerate(story_urls, 1):
        print(f"[{i}/{len(story_urls)}] Scraping {url}...")
        
        try:
            story = scrape_story(url, session)
            
            if story["text"]:
                doc = {
                    "id": f"storybooks_hz_{story['story_id']}",
                    "source": "storybooks_namibia",
                    "source_url": url,
                    "publisher": SOURCE_PUBLISHER,
                    "title": story["title"],
                    "author": story["author"],
                    "translator": story["translator"],
                    "text": story["text"],
                    "language": "hz",
                    "license": LICENSE,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                    "word_count": len(story["text"].split()),
                    "char_count": len(story["text"]),
                }
                all_documents.append(doc)
                
                total_chars += doc["char_count"]
                total_words += doc["word_count"]
                
                # Save individual file
                with open(output_path / f"story_{story['story_id']}.json", 'w', encoding='utf-8') as f:
                    json.dump(doc, f, ensure_ascii=False, indent=2)
                
                print(f"  ✓ '{story['title'][:40]}...' - {doc['char_count']} chars, {story['paragraphs']} paragraphs")
            else:
                print(f"  ⚠ No Herero text extracted")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        time.sleep(RATE_LIMIT)
    
    # Save combined JSONL
    with open(output_path / 'all_storybooks.jsonl', 'w', encoding='utf-8') as f:
        for doc in all_documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    # Save stats
    stats = {
        "process_date": datetime.now().strftime("%Y-%m-%d"),
        "source": "storybooks_namibia",
        "source_url": STORIES_URL,
        "license": LICENSE,
        "total_stories": len(all_documents),
        "total_characters": total_chars,
        "total_words": total_words,
    }
    
    with open(output_path / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"COMPLETE: {len(all_documents)} stories")
    print(f"Characters: {total_chars}")
    print(f"Words: {total_words}")
    print(f"Output: {output_path}")
    
    return stats


if __name__ == '__main__':
    import sys
    
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "data/raw/storybooks_namibia/2025-12-25"
    
    stats = process_all_stories(output_dir)
