"""
Dataset Curation - Refined English Removal

More conservative filtering to preserve Herero text.
Removes only clearly English content, not short words that
appear in both languages.

Outputs:
1. herero_pretraining_curated.jsonl - Clean Herero text
2. herero_removed_content.jsonl - What was removed (for review)
"""

import json
import re
from pathlib import Path
from datetime import datetime


# Strong English markers - words that rarely/never appear in Herero
# Removed short words: in, an, be, of, to, on, at, by, as, or, it, he, we, me
ENGLISH_STRONG = {
    'the', 'and', 'have', 'has', 'had', 'been', 'being', 'with', 'from',
    'that', 'this', 'these', 'those', 'what', 'which', 'where', 'when',
    'who', 'whom', 'whose', 'why', 'how', 'will', 'would', 'could', 'should',
    'shall', 'may', 'might', 'must', 'can', 'cannot', 'but', 'not',
    'you', 'your', 'they', 'them', 'their', 'about', 'after', 'before',
    'between', 'under', 'over', 'into', 'through', 'during', 'because',
    'although', 'however', 'therefore', 'also', 'only', 'just', 'very',
    'copyright', 'rights', 'reserved', 'download', 'click', 'here',
    'more', 'information', 'contact', 'email', 'website', 'page',
    'see', 'different', 'versions', 'related', 'audio', 'video',
    'using', 'creating', 'choosing', 'language', 'germans', 'german',
    'africa', 'namibia', 'botswana', 'people', 'population', 'region',
    'spoken', 'speak', 'dialect', 'genocide', 'colonial', 'military',
    'history', 'documents', 'references', 'bibliography', 'reading',
    'further', 'source', 'university', 'journal', 'london', 'berlin',
    'digitized', 'google', 'available', 'released', 'published',
}

# Herero-specific patterns - strong indicators
HERERO_PATTERNS = [
    r'\btj[aeiou]',       # tja, tji, tjo, tju, tje
    r'\bndj[aeiou]',      # ndja, ndji, etc.
    r'\bmb[aeiou]',       # mba, mbi, etc.
    r'\bng[aeiou]',       # nga, ngi, etc.
    r'\bov[aeiou]',       # ova, ovi, ovo
    r'\bok[aeiou]',       # oka, oku, oki
    r'\bom[aeiou]',       # oma, omu, omi
    r'\bor[aeiou]',       # oru, ora
    r'\bez[aeiou]',       # eza, ezo
    r'[ṱṋḓ]',            # Herero diacritics
    r'\bua\b',            # common Herero
    r'\bnu\b',            # "and" in Herero
    r'\bku\b',            # common
    r'\bmu\b',            # common
    r'\bwa\b',            # common
    r'\bya\b',            # common
    r'\bze\b',            # common
    r'\bvi\b',            # common
    r'\bvo\b',            # common
    r'\bje\b',            # common
    r'\bri\b',            # common
    r'\barire\b',         # Herero word
    r'\bkutja\b',         # Herero word
    r'\botji',            # Herero prefix
    r'\bomundu\b',        # person
    r'\bovandu\b',        # people
]

# Removal patterns (clearly not Herero content)
REMOVAL_PATTERNS = [
    r'References Bibliography.*',
    r'Further reading.*',
    r'ISBN\s*[\d\-X]+',
    r'http[s]?://\S+',
    r'www\.\S+',
    r'\[.*?\]\(.*?\)',    # Markdown links
]


def contains_non_latin(text: str) -> bool:
    """Check if text contains significant non-Latin scripts."""
    non_latin = re.findall(r'[^\u0000-\u024F\u1E00-\u1EFF\s\d.,!?;:\'"()\[\]{}@#$%^&*+=<>/-]', text)
    return len(non_latin) / max(len(text), 1) > 0.15  # Raised threshold


def count_english_words(sentence: str) -> int:
    """Count strong English marker words."""
    words = set(re.findall(r'\b[a-zA-Z]+\b', sentence.lower()))
    return len(words & ENGLISH_STRONG)


def count_herero_patterns(sentence: str) -> int:
    """Count Herero language patterns."""
    return sum(1 for p in HERERO_PATTERNS if re.search(p, sentence.lower()))


def should_remove(sentence: str) -> tuple:
    """
    Determine if sentence should be removed.
    Returns: (should_remove: bool, reason: str or None)
    """
    if not sentence or len(sentence) < 10:
        return False, None
    
    # Check for non-Latin scripts
    if contains_non_latin(sentence):
        return True, "non_latin_script"
    
    # Count markers
    english_count = count_english_words(sentence)
    herero_count = count_herero_patterns(sentence)
    word_count = len(sentence.split())
    
    # Decision logic:
    # - If many English words and few Herero patterns -> remove
    # - If Herero patterns present, be very careful
    
    if herero_count >= 2:
        # Strong Herero markers - keep unless overwhelmingly English
        if english_count >= 5 and english_count > herero_count * 2:
            return True, "english_detected"
        return False, None
    
    if herero_count == 1:
        # Some Herero markers - need significant English to remove
        if english_count >= 3:
            return True, "english_detected"
        return False, None
    
    # No Herero markers - even just 2 strong English words is suspicious
    if english_count >= 2:
        return True, "english_detected"
    
    return False, None


def clean_text_with_tracking(text: str) -> tuple:
    """
    Clean text and track what was removed.
    Returns: (cleaned_text, removed_sentences)
    """
    removed_sentences = []
    
    # Remove boilerplate patterns first
    for pattern in REMOVAL_PATTERNS:
        matches = re.findall(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        for m in matches:
            if m.strip() and len(m.strip()) > 5:
                removed_sentences.append({"text": m.strip(), "reason": "boilerplate_pattern"})
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Process paragraphs
    paragraphs = text.split('\n\n')
    cleaned_paragraphs = []
    
    for para in paragraphs:
        # Skip entirely non-Latin paragraphs
        if contains_non_latin(para):
            if len(para.strip()) > 20:
                removed_sentences.append({"text": para.strip()[:500], "reason": "non_latin_script"})
            continue
        
        sentences = re.split(r'(?<=[.!?])\s+', para)
        cleaned_sentences = []
        
        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 10:
                continue
            
            remove, reason = should_remove(sent)
            if remove:
                removed_sentences.append({"text": sent, "reason": reason})
            else:
                cleaned_sentences.append(sent)
        
        if cleaned_sentences:
            cleaned_para = ' '.join(cleaned_sentences)
            if len(cleaned_para.strip()) > 30:
                cleaned_paragraphs.append(cleaned_para)
    
    return '\n\n'.join(cleaned_paragraphs), removed_sentences


def curate_dataset(input_file: str, output_dir: str) -> dict:
    """Curate dataset with refined filtering."""
    
    print("="*60)
    print("DATASET CURATION (REFINED)")
    print("="*60 + "\n")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load
    docs = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))
    
    print(f"Loaded {len(docs)} documents")
    
    # Process
    original_chars = 0
    cleaned_chars = 0
    cleaned_docs = []
    all_removed = []
    
    for i, doc in enumerate(docs):
        text = doc.get('text', '')
        original_chars += len(text)
        
        cleaned_text, removed = clean_text_with_tracking(text)
        cleaned_chars += len(cleaned_text)
        
        for r in removed:
            r["source_doc_id"] = i
            all_removed.append(r)
        
        if cleaned_text and len(cleaned_text.strip()) > 50:
            cleaned_docs.append({"text": cleaned_text})
    
    # Save curated
    curated_file = output_path / 'herero_pretraining_curated.jsonl'
    with open(curated_file, 'w', encoding='utf-8') as f:
        for doc in cleaned_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    # Save removed
    removed_file = output_path / 'herero_removed_content.jsonl'
    with open(removed_file, 'w', encoding='utf-8') as f:
        for item in all_removed:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    # Stats
    removed_chars = original_chars - cleaned_chars
    removed_pct = (removed_chars / original_chars * 100) if original_chars > 0 else 0
    
    reason_counts = {}
    for r in all_removed:
        reason = r.get('reason', 'unknown')
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
    
    stats = {
        "created_at": datetime.now().isoformat(),
        "original_documents": len(docs),
        "cleaned_documents": len(cleaned_docs),
        "original_characters": original_chars,
        "cleaned_characters": cleaned_chars,
        "removed_characters": removed_chars,
        "removed_percentage": f"{removed_pct:.2f}%",
        "removed_items": len(all_removed),
        "removal_reasons": reason_counts,
    }
    
    with open(output_path / 'curation_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\nOriginal: {len(docs)} docs, {original_chars:,} chars")
    print(f"Cleaned:  {len(cleaned_docs)} docs, {cleaned_chars:,} chars")
    print(f"Removed:  {removed_chars:,} chars ({removed_pct:.2f}%)")
    print(f"\nRemoval breakdown:")
    for reason, count in sorted(reason_counts.items()):
        print(f"  - {reason}: {count}")
    
    return stats


if __name__ == '__main__':
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "data/processed/herero_pretraining.jsonl"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/processed"
    curate_dataset(input_file, output_dir)
