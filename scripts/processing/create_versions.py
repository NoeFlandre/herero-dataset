"""
Create Two Dataset Versions

1. HuggingFace version - Only clearly licensed sources (CC BY, Public Domain)
2. Local version - All content (for personal use only)
"""

import json
from pathlib import Path
from datetime import datetime

# Sources with CLEAR redistribution rights for HuggingFace
HUGGINGFACE_SAFE_SOURCES = [
    'wikipedia',        # CC BY-SA 3.0
    'bible',           # Public Domain (1849)
    'storybook',       # CC BY 3.0/4.0
    'omnilingual',     # CC BY 4.0
    'glotcc',          # CC BY 4.0
    'fineweb2',        # ODC-By 1.0
    'finepdfs',        # ODC-By 1.0
]

# Sources with unclear or NC licenses (local only)
LOCAL_ONLY_SOURCES = [
    'lac',             # Educational - unclear terms
    'constitution',    # Educational - unclear terms  
    'bcp',             # CC BY-NC-SA 4.0 - non-commercial
    'ovaherero',       # Same as bcp
]


def load_raw_data_by_source(raw_dir: str) -> dict:
    """Load raw data grouped by source."""
    
    raw_path = Path(raw_dir)
    sources = {}
    
    for jsonl_file in raw_path.rglob("*.jsonl"):
        source_name = jsonl_file.parent.parent.name
        
        docs = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    doc = json.loads(line)
                    docs.append(doc)
        
        if source_name not in sources:
            sources[source_name] = []
        sources[source_name].extend(docs)
    
    return sources


def is_huggingface_safe(source_name: str) -> bool:
    """Check if source is safe for HuggingFace distribution."""
    source_lower = source_name.lower()
    return any(safe in source_lower for safe in HUGGINGFACE_SAFE_SOURCES)


def clean_text(text: str) -> str:
    """Basic cleaning - remove obvious English/boilerplate."""
    import re
    
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    
    # Remove common boilerplate
    boilerplate = [
        r'References Bibliography.*',
        r'Further reading.*',
        r'ISBN\s*[\d\-X]+',
        r'\[.*?\]\(.*?\)',
    ]
    for pat in boilerplate:
        text = re.sub(pat, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Clean whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'  +', ' ', text)
    
    return text.strip()


def create_datasets(raw_dir: str, output_dir: str):
    """Create both dataset versions."""
    
    print("="*60)
    print("CREATING DATASET VERSIONS")
    print("="*60 + "\n")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load all data by source
    sources = load_raw_data_by_source(raw_dir)
    
    print("Sources found:")
    for name, docs in sorted(sources.items()):
        total_chars = sum(len(d.get('text', '')) for d in docs)
        safe = "✅ HF" if is_huggingface_safe(name) else "🏠 Local"
        print(f"  {safe} {name}: {len(docs)} docs, {total_chars:,} chars")
    
    # Create two versions
    hf_docs = []
    local_docs = []
    
    hf_chars = 0
    local_chars = 0
    
    for source_name, docs in sources.items():
        for doc in docs:
            text = doc.get('text', '')
            if not text or len(text) < 50:
                continue
            
            cleaned = clean_text(text)
            if len(cleaned) < 50:
                continue
            
            entry = {"text": cleaned, "source": source_name}
            
            # Add to local (everything)
            local_docs.append(entry)
            local_chars += len(cleaned)
            
            # Add to HuggingFace only if safe
            if is_huggingface_safe(source_name):
                hf_docs.append(entry)
                hf_chars += len(cleaned)
    
    # Save HuggingFace version
    hf_file = output_path / 'herero_huggingface.jsonl'
    with open(hf_file, 'w', encoding='utf-8') as f:
        for doc in hf_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    # Save local version
    local_file = output_path / 'herero_local_full.jsonl'
    with open(local_file, 'w', encoding='utf-8') as f:
        for doc in local_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    # Stats
    stats = {
        "created_at": datetime.now().isoformat(),
        "huggingface_version": {
            "file": str(hf_file),
            "documents": len(hf_docs),
            "characters": hf_chars,
            "license": "CC BY-SA 4.0",
            "sources": [s for s in sources.keys() if is_huggingface_safe(s)],
        },
        "local_version": {
            "file": str(local_file),
            "documents": len(local_docs),
            "characters": local_chars,
            "license": "Personal use only",
            "sources": list(sources.keys()),
        }
    }
    
    with open(output_path / 'dataset_versions.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    print(f"\n📤 HuggingFace Version (CC BY-SA 4.0):")
    print(f"   Documents: {len(hf_docs)}")
    print(f"   Characters: {hf_chars:,}")
    print(f"   File: {hf_file}")
    print(f"\n🏠 Local Version (Personal use):")
    print(f"   Documents: {len(local_docs)}")
    print(f"   Characters: {local_chars:,}")
    print(f"   File: {local_file}")
    print(f"\n   Difference: +{local_chars - hf_chars:,} chars in local version")
    
    return stats


if __name__ == '__main__':
    create_datasets("data/raw", "data/processed")
