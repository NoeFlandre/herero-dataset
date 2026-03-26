#!/usr/bin/env python3
"""
Build unified HuggingFace dataset from all 7 Herero sources.
Creates train/validation/test splits for research-grade quality.
"""

import json
import hashlib
import random
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Reproducible splits
RANDOM_SEED = 42

# Split ratios
TRAIN_RATIO = 0.90
VAL_RATIO = 0.05
TEST_RATIO = 0.05

# Source configurations
SOURCES = [
    {
        "path": "data/raw/wikipedia_hz/2025-12-24/all_articles.jsonl",
        "name": "wikipedia_incubator",
        "license": "CC BY-SA 3.0",
        "url_field": "source_url",
        "text_field": "text",
        "id_prefix": "wiki"
    },
    {
        "path": "data/raw/herero_bible/2025-12-24/all_bible.jsonl",
        "name": "herero_bible_1849",
        "license": "Public Domain",
        "url_field": "source_url",
        "text_field": "text",
        "id_prefix": "bible"
    },
    {
        "path": "data/raw/storybooks_namibia/2025-12-25/all_storybooks.jsonl",
        "name": "storybooks_namibia",
        "license": "CC BY 3.0/4.0",
        "url_field": "source_url",
        "text_field": "text",
        "id_prefix": "story"
    },
    {
        "path": "data/raw/omnilingual_hz/2025-12-25/all_omnilingual.jsonl",
        "name": "omnilingual_asr",
        "license": "CC BY 4.0",
        "url_field": "source_url",
        "text_field": "text",
        "id_prefix": "omni"
    },
    {
        "path": "data/raw/glotcc_hz/2025-12-25/all_glotcc.jsonl",
        "name": "glotcc_v1",
        "license": "CC BY 4.0",
        "url_field": "source_url",
        "text_field": "text",
        "id_prefix": "glot"
    },
    {
        "path": "data/raw/fineweb2_hz/2025-12-26/all_fineweb2.jsonl",
        "name": "fineweb2",
        "license": "ODC-By 1.0",
        "url_field": "url",
        "text_field": "text",
        "id_prefix": "fw2"
    },
    {
        "path": "data/raw/finepdfs_hz/2025-12-26/all_finepdfs.jsonl",
        "name": "finepdfs",
        "license": "ODC-By 1.0",
        "url_field": "url",
        "text_field": "text",
        "id_prefix": "fpdf"
    },
]

def text_hash(text: str) -> str:
    """Generate hash for deduplication."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())

def normalize_text(text: str) -> str:
    """Normalize text for consistency."""
    import unicodedata
    # NFC normalization
    text = unicodedata.normalize('NFC', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text.strip()

def stratified_split(docs_by_source: dict, train_ratio: float, val_ratio: float, test_ratio: float, seed: int):
    """
    Create stratified splits ensuring each source is represented in all splits.
    """
    random.seed(seed)
    
    train_docs = []
    val_docs = []
    test_docs = []
    
    for source_name, docs in docs_by_source.items():
        # Shuffle documents for this source
        shuffled = docs.copy()
        random.shuffle(shuffled)
        
        n = len(shuffled)
        n_val = max(1, int(n * val_ratio)) if n >= 3 else 0
        n_test = max(1, int(n * test_ratio)) if n >= 3 else 0
        n_train = n - n_val - n_test
        
        # Ensure at least 1 document in train
        if n_train < 1 and n > 0:
            n_train = n
            n_val = 0
            n_test = 0
        
        train_docs.extend(shuffled[:n_train])
        val_docs.extend(shuffled[n_train:n_train + n_val])
        test_docs.extend(shuffled[n_train + n_val:])
    
    # Shuffle final splits
    random.shuffle(train_docs)
    random.shuffle(val_docs)
    random.shuffle(test_docs)
    
    return train_docs, val_docs, test_docs

def process_sources(base_path: Path, output_dir: Path):
    """Process all sources and write train/val/test JSONL files."""
    
    seen_hashes = set()
    docs_by_source = defaultdict(list)
    stats = {
        "total_docs": 0,
        "duplicates_removed": 0,
        "min_length_filtered": 0,
        "by_source": {},
        "splits": {}
    }
    
    print("📖 Reading and processing sources...\n")
    
    for source_config in SOURCES:
        source_path = base_path / source_config["path"]
        source_name = source_config["name"]
        
        if not source_path.exists():
            print(f"⚠️  Skipping {source_name}: file not found at {source_path}")
            continue
        
        source_stats = {"docs": 0, "words": 0, "chars": 0, "duplicates": 0, "filtered": 0}
        doc_idx = 0
        
        with open(source_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    doc = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                # Extract and normalize text
                text = doc.get(source_config["text_field"], "")
                if not text:
                    continue
                
                text = normalize_text(text)
                
                # Minimum length filter (50 chars)
                if len(text) < 50:
                    source_stats["filtered"] += 1
                    stats["min_length_filtered"] += 1
                    continue
                
                # Deduplicate using hash
                h = text_hash(text)
                if h in seen_hashes:
                    source_stats["duplicates"] += 1
                    stats["duplicates_removed"] += 1
                    continue
                seen_hashes.add(h)
                
                # Get URL
                url = doc.get(source_config["url_field"], "")
                if not url:
                    url = doc.get("url", doc.get("source_url", ""))
                
                # Calculate statistics
                doc_idx += 1
                word_count = count_words(text)
                char_count = len(text)
                
                # Create normalized document
                normalized = {
                    "id": f"{source_config['id_prefix']}_{doc_idx:05d}",
                    "text": text,
                    "source": source_name,
                    "url": url,
                    "license": source_config["license"],
                    "word_count": word_count,
                    "char_count": char_count
                }
                
                docs_by_source[source_name].append(normalized)
                source_stats["docs"] += 1
                source_stats["words"] += word_count
                source_stats["chars"] += char_count
        
        stats["by_source"][source_name] = source_stats
        print(f"✅ {source_name}: {source_stats['docs']} docs, {source_stats['words']:,} words" + 
              (f" ({source_stats['duplicates']} dupes)" if source_stats['duplicates'] else ""))
    
    # Create stratified splits
    print("\n🔀 Creating stratified train/val/test splits...")
    train_docs, val_docs, test_docs = stratified_split(
        docs_by_source, TRAIN_RATIO, VAL_RATIO, TEST_RATIO, RANDOM_SEED
    )
    
    # Write output files
    output_dir.mkdir(parents=True, exist_ok=True)
    splits = {
        "train": train_docs,
        "validation": val_docs,
        "test": test_docs
    }
    
    for split_name, docs in splits.items():
        output_path = output_dir / f"{split_name}.jsonl"
        with open(output_path, 'w', encoding='utf-8') as f:
            for doc in docs:
                f.write(json.dumps(doc, ensure_ascii=False) + '\n')
        
        split_words = sum(d["word_count"] for d in docs)
        split_chars = sum(d["char_count"] for d in docs)
        stats["splits"][split_name] = {
            "docs": len(docs),
            "words": split_words,
            "chars": split_chars
        }
        print(f"   {split_name}: {len(docs):,} docs, {split_words:,} words")
    
    # Calculate totals
    stats["total_docs"] = sum(len(docs) for docs in splits.values())
    stats["total_words"] = sum(s["words"] for s in stats["splits"].values())
    stats["total_chars"] = sum(s["chars"] for s in stats["splits"].values())
    stats["random_seed"] = RANDOM_SEED
    stats["split_ratios"] = {"train": TRAIN_RATIO, "validation": VAL_RATIO, "test": TEST_RATIO}
    stats["created_at"] = datetime.utcnow().isoformat() + "Z"
    
    print(f"\n📊 Total: {stats['total_docs']:,} docs, {stats['total_words']:,} words, {stats['total_chars']:,} chars")
    print(f"🔄 Duplicates removed: {stats['duplicates_removed']}")
    print(f"📏 Min-length filtered: {stats['min_length_filtered']}")
    
    # Write comprehensive stats
    stats_path = output_dir.parent / "dataset_info.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    return stats

if __name__ == "__main__":
    base_path = Path(__file__).parent.parent
    output_dir = base_path / "huggingface_dataset" / "data"
    
    print("🚀 Building Research-Grade Herero HuggingFace Dataset")
    print("=" * 55)
    print(f"   Random seed: {RANDOM_SEED}")
    print(f"   Splits: {TRAIN_RATIO:.0%} train / {VAL_RATIO:.0%} val / {TEST_RATIO:.0%} test")
    print("=" * 55 + "\n")
    
    stats = process_sources(base_path, output_dir)
    
    print(f"\n✅ Dataset written to: {output_dir}")
    print(f"   - train.jsonl")
    print(f"   - validation.jsonl")
    print(f"   - test.jsonl")
