"""
FineWeb-2 Herero Data Processor

Processes parquet files from HuggingFaceFW/fineweb-2 her_Latn subset.
License: ODC-By 1.0 - Can be used for HuggingFace publication.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd


def process_fineweb2(input_files: list, output_dir: str) -> dict:
    """Process FineWeb-2 parquet files."""
    
    print("="*60)
    print("FINEWEB-2 HERERO PROCESSOR")
    print("="*60 + "\n")
    
    output_path = Path(output_dir) / datetime.now().strftime("%Y-%m-%d")
    output_path.mkdir(parents=True, exist_ok=True)
    
    all_texts = []
    
    for file_path in input_files:
        print(f"Processing {Path(file_path).name}...")
        
        df = pd.read_parquet(file_path)
        print(f"  Columns: {list(df.columns)}")
        print(f"  Rows: {len(df)}")
        
        # Find text column
        text_col = None
        for col in ['text', 'content', 'raw_text', 'document']:
            if col in df.columns:
                text_col = col
                break
        
        if text_col is None:
            print(f"  ⚠️ No text column found, skipping")
            continue
        
        # Extract texts
        for idx, row in df.iterrows():
            text = row[text_col]
            if text and len(str(text)) > 50:
                entry = {
                    "text": str(text),
                    "source": "fineweb-2",
                }
                # Add any available metadata
                for col in ['url', 'id', 'language']:
                    if col in df.columns and pd.notna(row[col]):
                        entry[col] = str(row[col])
                
                all_texts.append(entry)
    
    # Deduplicate
    seen = set()
    unique_texts = []
    for t in all_texts:
        text_hash = hash(t['text'][:500])
        if text_hash not in seen:
            seen.add(text_hash)
            unique_texts.append(t)
    
    print(f"\nTotal extracted: {len(all_texts)}")
    print(f"Unique texts: {len(unique_texts)}")
    
    # Save
    output_file = output_path / "all_fineweb2.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for t in unique_texts:
            f.write(json.dumps(t, ensure_ascii=False) + '\n')
    
    total_chars = sum(len(t['text']) for t in unique_texts)
    total_words = sum(len(t['text'].split()) for t in unique_texts)
    
    stats = {
        "processed_at": datetime.now().isoformat(),
        "source": "HuggingFaceFW/fineweb-2 (her_Latn)",
        "license": "ODC-By 1.0",
        "can_redistribute": True,
        "documents": len(unique_texts),
        "total_characters": total_chars,
        "total_words": total_words,
    }
    
    with open(output_path / "stats.json", 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n{'='*60}")
    print("COMPLETE!")
    print(f"Documents: {len(unique_texts)}")
    print(f"Characters: {total_chars:,}")
    print(f"Words: {total_words:,}")
    print(f"Output: {output_file}")
    print(f"{'='*60}")
    
    return stats


if __name__ == '__main__':
    # Find parquet files
    root = Path(".")
    parquet_files = list(root.glob("*.parquet")) + list(root.glob("*FineWeb*.parquet"))
    
    if not parquet_files:
        print("No parquet files found in current directory")
        sys.exit(1)
    
    print(f"Found parquet files: {[f.name for f in parquet_files]}")
    process_fineweb2([str(f) for f in parquet_files], "data/raw/fineweb2_hz")
