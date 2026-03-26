"""
FinePDFs Herero Data Processor

Processes parquet file from HuggingFaceFW/finepdfs her_Latn subset.
License: ODC-By 1.0 - Can be used for HuggingFace publication.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd


def process_finepdfs(input_file: str, output_dir: str) -> dict:
    """Process FinePDFs parquet file."""
    
    print("="*60)
    print("FINEPDFS HERERO PROCESSOR")
    print("="*60 + "\n")
    
    output_path = Path(output_dir) / datetime.now().strftime("%Y-%m-%d")
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing {Path(input_file).name}...")
    
    df = pd.read_parquet(input_file)
    print(f"  Columns: {list(df.columns)}")
    print(f"  Rows: {len(df)}")
    
    # Find text column
    text_col = None
    for col in ['text', 'content', 'raw_text', 'document', 'pdf_text']:
        if col in df.columns:
            text_col = col
            break
    
    if text_col is None:
        print(f"  ⚠️ No text column found")
        print(f"  Available columns: {list(df.columns)}")
        return None
    
    # Extract texts
    all_texts = []
    for idx, row in df.iterrows():
        text = row[text_col]
        if text and len(str(text)) > 50:
            entry = {
                "text": str(text),
                "source": "finepdfs",
            }
            # Add any available metadata
            for col in ['url', 'id', 'language', 'pdf_url']:
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
    output_file = output_path / "all_finepdfs.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for t in unique_texts:
            f.write(json.dumps(t, ensure_ascii=False) + '\n')
    
    total_chars = sum(len(t['text']) for t in unique_texts)
    total_words = sum(len(t['text'].split()) for t in unique_texts)
    
    stats = {
        "processed_at": datetime.now().isoformat(),
        "source": "HuggingFaceFW/finepdfs (her_Latn)",
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
    # Find parquet file
    root = Path(".")
    parquet_files = list(root.glob("*FinePDF*.parquet")) + list(root.glob("*finepdfs*.parquet"))
    
    if not parquet_files:
        print("No FinePDFs parquet files found")
        sys.exit(1)
    
    print(f"Found: {parquet_files[0].name}")
    process_finepdfs(str(parquet_files[0]), "data/raw/finepdfs_hz")
