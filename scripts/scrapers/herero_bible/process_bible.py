"""
Herero Bible Processing Script

Cleans and processes the herero-bible.txt file from Archive.org.
Removes OCR artifacts, page markers, and extracts content into structured format.
"""

import json
import re
from pathlib import Path
from datetime import datetime


# Source metadata
SOURCE_URL = "https://archive.org/stream/OmahungiOaEmboRaJehovaNaOmaimpurir/Omahungi_oa_Embo_ra_Jehova_na_omaimpurir_djvu.txt"
SOURCE_TITLE = "Omahungi Oa Embo Ra Jehova Na Omaimpuriro Mo Otjiherero"
SOURCE_YEAR = 1849
LICENSE = "Public Domain"  # 1849 publication is in public domain


def clean_text(text: str) -> str:
    """Clean OCR artifacts and normalize text."""
    
    # Remove "Digitized by Google" lines (various forms)
    text = re.sub(r'Digitized by\s*\n*\s*Google', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Digitized by Google', '', text, flags=re.IGNORECASE)
    
    # Remove page numbers (standalone numbers like "2", "10", "17")
    text = re.sub(r'^\s*\d{1,3}\s*$', '', text, flags=re.MULTILINE)
    
    # Remove single letters on lines (OCR artifacts like "A", "B")
    text = re.sub(r'^\s*[A-Z]\s*$', '', text, flags=re.MULTILINE)
    
    # Remove lines with only special characters
    text = re.sub(r'^\s*[<>\.;:,\-\*]+\s*$', '', text, flags=re.MULTILINE)
    
    # Remove orphaned line fragments
    text = re.sub(r'^\s*[A-Z]\s*\n', '\n', text, flags=re.MULTILINE)
    
    # Remove multiple blank lines (keep max 2)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # Remove lines that are just musical notation markers like [Vorige Weise.]
    text = re.sub(r'\[.*Weise.*\]', '', text)
    text = re.sub(r'\[.*\.\]', '', text)
    
    # Clean up trailing artifacts at end
    text = re.sub(r'[/\\V\s\.\!"]+$', '', text)
    
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r' +\n', '\n', text)
    
    return text.strip()


def extract_sections(text: str) -> list:
    """Extract stories (EHUNGI) and hymns (OMAIMPURIRO) as separate sections."""
    
    sections = []
    
    # Split into stories section and hymns section
    hymns_marker = "0MAIMPU1IIR0"  # OCR variant
    hymns_alt = "OMAIMPURIRO"
    
    if hymns_marker in text:
        stories_part, hymns_part = text.split(hymns_marker, 1)
    elif hymns_alt in text:
        stories_part, hymns_part = text.split(hymns_alt, 1)
    else:
        stories_part = text
        hymns_part = ""
    
    # Extract individual stories (EHUNGI I, II, III, etc.)
    story_pattern = r'(EHUNGI\s+[IVXLC]+\.?\s*\n.*?)(?=EHUNGI\s+[IVXLC]+\.?\s*\n|$)'
    stories = re.findall(story_pattern, stories_part, re.DOTALL)
    
    for i, story in enumerate(stories, 1):
        # Get title from first line
        lines = story.strip().split('\n')
        title_line = lines[0] if lines else f"Story {i}"
        
        # Get subtitle if present (e.g., "Orutenga. 1 Mose 1.2")
        subtitle = ""
        if len(lines) > 1:
            for line in lines[1:5]:
                if line.strip() and not line.strip().startswith('Ero'):
                    subtitle = line.strip()
                    break
        
        cleaned = clean_text(story)
        if len(cleaned) > 50:  # Only include substantial content
            sections.append({
                "type": "story",
                "number": i,
                "title": title_line.strip(),
                "subtitle": subtitle,
                "text": cleaned,
            })
    
    # Extract hymns (numbered 1., 2., 3., etc.)
    if hymns_part:
        hymn_pattern = r'(\d+\s*\.\s*\n.*?)(?=\d+\s*\.\s*\n|$)'
        hymns = re.findall(hymn_pattern, hymns_part, re.DOTALL)
        
        for i, hymn in enumerate(hymns, 1):
            cleaned = clean_text(hymn)
            if len(cleaned) > 20:
                sections.append({
                    "type": "hymn",
                    "number": i,
                    "title": f"Hymn {i}",
                    "subtitle": "",
                    "text": cleaned,
                })
    
    return sections


def process_bible(input_path: str, output_dir: str) -> dict:
    """Process the Herero Bible file and output structured data."""
    
    # Read input
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    # Clean the entire text first
    cleaned_full = clean_text(raw_text)
    
    # Extract sections
    sections = extract_sections(raw_text)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Prepare documents
    documents = []
    stories_count = 0
    hymns_count = 0
    
    for i, section in enumerate(sections, 1):
        doc = {
            "id": f"bible_hz_{i:03d}",
            "source": "herero_bible_1849",
            "source_url": SOURCE_URL,
            "title": section["title"],
            "subtitle": section.get("subtitle", ""),
            "section_type": section["type"],
            "section_number": section["number"],
            "text": section["text"],
            "language": "hz",
            "license": LICENSE,
            "year": SOURCE_YEAR,
            "scraped_at": datetime.utcnow().isoformat() + 'Z',
            "word_count": len(section["text"].split()),
            "char_count": len(section["text"]),
        }
        documents.append(doc)
        
        if section["type"] == "story":
            stories_count += 1
        else:
            hymns_count += 1
    
    # Save individual JSON files
    for doc in documents:
        filename = f"{doc['id']}_{doc['section_type']}.json"
        with open(output_path / filename, 'w', encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
    
    # Save combined JSONL
    jsonl_path = output_path / 'all_bible.jsonl'
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    # Save cleaned full text
    with open(output_path / 'herero_bible_cleaned.txt', 'w', encoding='utf-8') as f:
        f.write(cleaned_full)
    
    # Calculate stats
    total_chars = sum(d['char_count'] for d in documents)
    total_words = sum(d['word_count'] for d in documents)
    
    stats = {
        "process_date": datetime.now().strftime("%Y-%m-%d"),
        "source": "herero_bible_1849",
        "source_url": SOURCE_URL,
        "original_year": SOURCE_YEAR,
        "license": LICENSE,
        "total_sections": len(documents),
        "stories_count": stories_count,
        "hymns_count": hymns_count,
        "total_characters": total_chars,
        "total_words": total_words,
        "avg_chars_per_section": total_chars // len(documents) if documents else 0,
    }
    
    with open(output_path / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Processed {len(documents)} sections ({stories_count} stories, {hymns_count} hymns)")
    print(f"Total: {total_chars} characters, {total_words} words")
    print(f"Output: {output_path}")
    
    return stats


if __name__ == '__main__':
    import sys
    
    # Default paths
    input_file = "herero-bible.txt"
    output_dir = "data/raw/herero_bible/2025-12-24"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    stats = process_bible(input_file, output_dir)
    print("\nStats:", json.dumps(stats, indent=2))
