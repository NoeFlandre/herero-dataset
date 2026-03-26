"""
GlotCC Parquet Processing Script

Extracts Herero text from GlotCC-V1 dataset.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone


SOURCE_URL = "https://huggingface.co/datasets/cis-lmu/GlotCC-V1"
LICENSE = "CC BY 4.0"  # GlotCC uses CC BY


def process_glotcc(input_dir: str, output_dir: str) -> dict:
    """Process GlotCC parquet files."""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    parquet_files = list(input_path.glob("*.parquet"))
    print(f"Found {len(parquet_files)} parquet files\n")
    
    all_texts = []
    total_rows = 0
    
    for pf in parquet_files:
        print(f"Processing {pf.name}...")
        
        df = pd.read_parquet(pf)
        total_rows += len(df)
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        
        # Extract text column - GlotCC uses 'content'
        text_col = None
        for col in ['content', 'text']:
            if col in df.columns:
                text_col = col
                break
        
        if text_col:
            texts = df[text_col].dropna().tolist()
            all_texts.extend(texts)
            print(f"  Extracted {len(texts)} texts from '{text_col}'")
    
    # Create documents
    documents = []
    for i, text in enumerate(all_texts, 1):
        if text and len(text.strip()) > 20:
            doc = {
                "id": f"glotcc_hz_{i:05d}",
                "source": "glotcc_v1",
                "source_url": SOURCE_URL,
                "text": text.strip(),
                "language": "hz",
                "license": LICENSE,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
                "word_count": len(text.split()),
                "char_count": len(text),
            }
            documents.append(doc)
    
    # Save JSONL
    with open(output_path / 'all_glotcc.jsonl', 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    # Stats
    total_chars = sum(d['char_count'] for d in documents)
    total_words = sum(d['word_count'] for d in documents)
    
    stats = {
        "process_date": datetime.now().strftime("%Y-%m-%d"),
        "source": "glotcc_v1",
        "source_url": SOURCE_URL,
        "license": LICENSE,
        "parquet_files": len(parquet_files),
        "total_rows": total_rows,
        "documents": len(documents),
        "total_characters": total_chars,
        "total_words": total_words,
    }
    
    with open(output_path / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"COMPLETE: {len(documents)} documents")
    print(f"Characters: {total_chars}")
    print(f"Words: {total_words}")
    
    return stats


if __name__ == '__main__':
    import sys
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "to_be_processed"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/raw/glotcc_hz/2025-12-25"
    process_glotcc(input_dir, output_dir)
