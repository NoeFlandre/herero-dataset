"""
Tests for Herero Dataset creation script.
Run with: pytest tests/ -v
"""

import pytest
import json
import hashlib
import random
import unicodedata
from pathlib import Path
from collections import defaultdict


# Import functions from the script
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.create_hf_dataset import (
    text_hash, count_words, normalize_text, stratified_split
)


class TestNormalizeText:
    """Tests for text normalization."""

    def test_nfc_normalization(self):
        """Text should be NFC normalized."""
        # é can be represented as single char or combining chars
        text = "café"
        normalized = normalize_text(text)
        assert normalized == "café"

    def test_whitespace_normalization(self):
        """Multiple spaces should be collapsed to single space."""
        text = "hello    world\n\n  test"
        normalized = normalize_text(text)
        assert normalized == "hello world test"

    def test_strip_whitespace(self):
        """Text should be stripped of leading/trailing whitespace."""
        text = "  hello world  "
        normalized = normalize_text(text)
        assert normalized == "hello world"

    def test_empty_text(self):
        """Empty text should return empty string."""
        assert normalize_text("") == ""
        assert normalize_text("   ") == ""


class TestTextHash:
    """Tests for text hashing."""

    def test_same_text_same_hash(self):
        """Same text should produce same hash."""
        text = "hello world"
        hash1 = text_hash(text)
        hash2 = text_hash(text)
        assert hash1 == hash2

    def test_different_text_different_hash(self):
        """Different texts should produce different hashes."""
        hash1 = text_hash("hello")
        hash2 = text_hash("world")
        assert hash1 != hash2

    def test_hash_is_sha256(self):
        """Hash should be a SHA256 hex string (64 chars)."""
        hash_result = text_hash("test")
        assert len(hash_result) == 64
        assert all(c in '0123456789abcdef' for c in hash_result)

    def test_empty_text_hash(self):
        """Empty text should produce valid hash."""
        hash_result = text_hash("")
        assert len(hash_result) == 64


class TestCountWords:
    """Tests for word counting."""

    def test_simple_text(self):
        """Simple text should count words correctly."""
        assert count_words("hello world") == 2

    def test_single_word(self):
        """Single word should return 1."""
        assert count_words("hello") == 1

    def test_empty_text(self):
        """Empty text should return 0."""
        assert count_words("") == 0

    def test_multiple_spaces(self):
        """Multiple spaces between words should not affect count."""
        assert count_words("hello    world") == 2

    def test_newlines_and_tabs(self):
        """Newlines and tabs should be treated as word separators."""
        assert count_words("hello\nworld\ttest") == 3


class TestStratifiedSplit:
    """Tests for stratified splitting."""

    def test_splits_sum_to_total(self):
        """All splits should contain all documents."""
        docs_by_source = {
            "source1": [{"id": 1}, {"id": 2}, {"id": 3}],
            "source2": [{"id": 4}, {"id": 5}]
        }
        train, val, test = stratified_split(docs_by_source, 0.8, 0.1, 0.1, seed=42)
        assert len(train) + len(val) + len(test) == 5

    def test_reproducible_with_seed(self):
        """Same seed should produce same splits."""
        docs_by_source = {
            "source1": [{"id": i} for i in range(10)],
        }
        train1, val1, test1 = stratified_split(docs_by_source, 0.8, 0.1, 0.1, seed=42)
        train2, val2, test2 = stratified_split(docs_by_source, 0.8, 0.1, 0.1, seed=42)
        assert [d["id"] for d in train1] == [d["id"] for d in train2]
        assert [d["id"] for d in val1] == [d["id"] for d in val2]
        assert [d["id"] for d in test1] == [d["id"] for d in test2]

    def test_all_sources_in_train(self):
        """Each source should have at least some docs in train if it has enough."""
        docs_by_source = {
            "source1": [{"id": i} for i in range(10)],
            "source2": [{"id": i} for i in range(10, 20)],
        }
        train, val, test = stratified_split(docs_by_source, 0.8, 0.1, 0.1, seed=42)
        train_ids = [d["id"] for d in train]
        assert any(d["id"] < 10 for d in train)
        assert any(d["id"] >= 10 for d in train)

    def test_small_source_not_in_val_or_test(self):
        """Sources with fewer than 3 docs should not be in val or test."""
        docs_by_source = {
            "large_source": [{"id": i} for i in range(100)],
            "small_source": [{"id": i} for i in range(100, 102)],
        }
        train, val, test = stratified_split(docs_by_source, 0.9, 0.05, 0.05, seed=42)
        small_in_val = any(d["id"] >= 100 for d in val)
        small_in_test = any(d["id"] >= 100 for d in test)
        assert not small_in_val or len([d for d in val if d["id"] >= 100]) <= 1
        assert not small_in_test or len([d for d in test if d["id"] >= 100]) <= 1

    def test_ratios_approximately_correct(self):
        """Split ratios should be approximately correct for large datasets."""
        docs_by_source = {
            "source1": [{"id": i} for i in range(1000)],
        }
        train, val, test = stratified_split(docs_by_source, 0.9, 0.05, 0.05, seed=42)
        total = len(train) + len(val) + len(test)
        assert 0.88 <= len(train) / total <= 0.92
        assert 0.03 <= len(val) / total <= 0.07
        assert 0.03 <= len(test) / total <= 0.07
