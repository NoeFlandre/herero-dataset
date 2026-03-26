"""
Omnilingual Parquet Processing Script

Extracts Herero (hz) text data from Meta Omnilingual ASR Corpus parquet files.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone


SOURCE_URL = "https://huggingface.co/datasets/Sellopale/omnilingualpaleoi"
ORIGINAL_SOURCE = "facebook/omnilingual-asr-corpus"
LICENSE = "Meta Research License"  # Check actual license


def process_parquet_files(input_dir: str, output_dir: str, language_code: str = "hz") -> dict:
    """Process parquet files and extract Herero data."""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all parquet files
    parquet_files = list(input_path.glob("*.parquet"))
    print(f"Found {len(parquet_files)} parquet files\n")
    
    all_texts = []
    total_rows = 0
    hz_rows = 0
    
    for pf in parquet_files:
        print(f"Processing {pf.name}...")
        
        try:
            df = pd.read_parquet(pf)
            total_rows += len(df)
            
            # Print columns to understand structure
            print(f"  Columns: {list(df.columns)}")
            print(f"  Total rows: {len(df)}")
            
            # Look for language column
            lang_col = None
            for col in ['language', 'lang', 'locale', 'language_code', 'lang_code']:
                if col in df.columns:
                    lang_col = col
                    break
            
            if lang_col:
                # Filter for Herero - ISO 639-3 is 'her', ISO 639-1 is 'hz'
                hz_mask = (df[lang_col].str.startswith('her', na=False) | 
                           df[lang_col].str.startswith('hz', na=False))
                if hz_mask.any():
                    hz_df = df[hz_mask]
                    hz_rows += len(hz_df)
                    print(f"  Found {len(hz_df)} Herero rows")
                    
                    # Extract text - prioritize raw_text
                    text_col = None
                    for col in ['raw_text', 'text', 'sentence', 'transcription', 'transcript', 'normalized_text']:
                        if col in df.columns:
                            text_col = col
                            break
                    
                    if text_col:
                        texts = hz_df[text_col].dropna().tolist()
                        all_texts.extend(texts)
                        print(f"  Extracted {len(texts)} texts from '{text_col}'")
                else:
                    # Print unique languages to see what's available
                    unique_langs = df[lang_col].unique()[:20]
                    print(f"  Languages in file (sample): {list(unique_langs)}")
            else:
                print(f"  No language column found, extracting all text...")
                # Try to extract all text if no language filtering
                for col in ['raw_text', 'text', 'sentence', 'transcription', 'transcript']:
                    if col in df.columns:
                        texts = df[col].dropna().tolist()
                        all_texts.extend(texts)
                        print(f"  Extracted {len(texts)} texts from '{col}'")
                        break
                        
        except Exception as e:
            print(f"  Error: {e}")
    
    # Remove duplicates
    unique_texts = list(set(all_texts))
    print(f"\nUnique texts: {len(unique_texts)}")
    
    # Create documents
    documents = []
    for i, text in enumerate(unique_texts, 1):
        if text and len(text.strip()) > 5:
            doc = {
                "id": f"omnilingual_hz_{i:05d}",
                "source": "omnilingual_asr_corpus",
                "source_url": SOURCE_URL,
                "original_source": ORIGINAL_SOURCE,
                "text": text.strip(),
                "language": "hz",
                "license": LICENSE,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
                "word_count": len(text.split()),
                "char_count": len(text),
            }
            documents.append(doc)
    
    # Save JSONL
    with open(output_path / 'all_omnilingual.jsonl', 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    # Save combined text
    full_text = "\n\n".join([d['text'] for d in documents])
    with open(output_path / 'omnilingual_hz_text.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    # Stats
    total_chars = sum(d['char_count'] for d in documents)
    total_words = sum(d['word_count'] for d in documents)
    
    stats = {
        "process_date": datetime.now().strftime("%Y-%m-%d"),
        "source": "omnilingual_asr_corpus",
        "source_url": SOURCE_URL,
        "parquet_files": len(parquet_files),
        "total_parquet_rows": total_rows,
        "herero_rows": hz_rows,
        "unique_texts": len(documents),
        "total_characters": total_chars,
        "total_words": total_words,
    }
    
    with open(output_path / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"COMPLETE: {len(documents)} texts")
    print(f"Characters: {total_chars}")
    print(f"Words: {total_words}")
    print(f"Output: {output_path}")
    
    return stats


if __name__ == '__main__':
    import sys
    
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "to_be_processed"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/raw/omnilingual_hz/2025-12-25"
    
    stats = process_parquet_files(input_dir, output_dir)
