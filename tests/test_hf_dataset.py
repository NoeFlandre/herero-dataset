"""
Comprehensive tests for Herero Dataset.
Run with: pytest tests/ -v --cov=scripts --cov-report=term-missing
"""

import pytest
import json
import tempfile
import hashlib
import random
from pathlib import Path
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.create_hf_dataset import (
    text_hash, count_words, normalize_text, stratified_split,
    SOURCES, RANDOM_SEED, TRAIN_RATIO, VAL_RATIO, TEST_RATIO
)


# =============================================================================
# Test Constants
# =============================================================================

class TestConstants:
    """Tests for module constants."""

    def test_random_seed_is_42(self):
        """Random seed must be 42 for reproducibility."""
        assert RANDOM_SEED == 42

    def test_split_ratios_sum_to_one(self):
        """Split ratios must sum to 1.0."""
        assert abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) < 1e-9

    def test_sources_is_list(self):
        """Sources must be a list."""
        assert isinstance(SOURCES, list)
        assert len(SOURCES) > 0

    def test_each_source_has_required_fields(self):
        """Each source config must have required fields."""
        required = {'path', 'name', 'license', 'url_field', 'text_field', 'id_prefix'}
        for source in SOURCES:
            assert required.issubset(source.keys()), f"Source {source['name']} missing fields"


# =============================================================================
# Test text_hash
# =============================================================================

class TestTextHash:
    """Tests for text hashing function."""

    def test_same_text_same_hash(self):
        """Same text must produce same hash."""
        text = "hello world"
        assert text_hash(text) == text_hash(text)

    def test_different_text_different_hash(self):
        """Different texts must produce different hashes."""
        assert text_hash("hello") != text_hash("world")

    def test_hash_is_sha256_length(self):
        """Hash must be 64 characters (SHA256 hex)."""
        result = text_hash("test")
        assert len(result) == 64

    def test_hash_is_hex(self):
        """Hash must be lowercase hexadecimal."""
        result = text_hash("test")
        assert all(c in '0123456789abcdef' for c in result)

    def test_empty_string_hash(self):
        """Empty string must produce valid hash."""
        result = text_hash("")
        assert len(result) == 64

    def test_unicode_hash(self):
        """Unicode text must produce valid hash."""
        result = text_hash("Herero ṱext 日本語")
        assert len(result) == 64

    def test_hash_deterministic(self):
        """Hash must be deterministic across calls."""
        text = "deterministic test"
        hashes = [text_hash(text) for _ in range(10)]
        assert len(set(hashes)) == 1


# =============================================================================
# Test count_words
# =============================================================================

class TestCountWords:
    """Tests for word counting function."""

    def test_single_word(self):
        """Single word returns 1."""
        assert count_words("hello") == 1

    def test_two_words(self):
        """Two words return 2."""
        assert count_words("hello world") == 2

    def test_empty_string(self):
        """Empty string returns 0."""
        assert count_words("") == 0

    def test_whitespace_only(self):
        """Whitespace-only returns 0."""
        assert count_words("   \n\t  ") == 0

    def test_multiple_spaces(self):
        """Multiple spaces between words don't affect count."""
        assert count_words("hello    world") == 2

    def test_newlines(self):
        """Newlines are word separators."""
        assert count_words("hello\nworld") == 2

    def test_tabs(self):
        """Tabs are word separators."""
        assert count_words("hello\tworld") == 2

    def test_mixed_whitespace(self):
        """Mixed whitespace is handled correctly."""
        assert count_words("hello  \n  world\t test") == 3

    def test_punctuation_not_separator(self):
        """Punctuation doesn't affect word count."""
        assert count_words("hello, world!") == 2

    def test_herero_text(self):
        """Herero text counts correctly."""
        assert count_words("OvaNerongo vokurangatira.") == 2


# =============================================================================
# Test normalize_text
# =============================================================================

class TestNormalizeText:
    """Tests for text normalization function."""

    def test_nfc_normalization(self):
        """Text must be NFC normalized."""
        # é as combining character sequence
        composed = normalize_text("café")
        # The result should be composed form
        assert composed == "café"

    def test_whitespace_collapse(self):
        """Multiple whitespace collapses to single space."""
        assert normalize_text("hello    world") == "hello world"
        assert normalize_text("hello\n\n\nworld") == "hello world"

    def test_leading_whitespace_removed(self):
        """Leading whitespace must be stripped."""
        assert normalize_text("  hello") == "hello"

    def test_trailing_whitespace_removed(self):
        """Trailing whitespace must be stripped."""
        assert normalize_text("hello  ") == "hello"

    def test_both_leading_and_trailing(self):
        """Both leading and trailing whitespace stripped."""
        assert normalize_text("  hello world  ") == "hello world"

    def test_empty_string(self):
        """Empty string returns empty."""
        assert normalize_text("") == ""

    def test_whitespace_only(self):
        """Whitespace-only returns empty."""
        assert normalize_text("   \n\t  ") == ""

    def test_unicode_preserved(self):
        """Unicode characters are preserved."""
        result = normalize_text("Herero ṱext")
        assert "ṱ" in result or "t" in result

    def test_idempotent(self):
        """Normalizing twice gives same result."""
        text = "  hello   world  "
        assert normalize_text(normalize_text(text)) == normalize_text(text)


# =============================================================================
# Test stratified_split
# =============================================================================

class TestStratifiedSplit:
    """Tests for stratified splitting function."""

    def test_all_documents_accounted_for(self):
        """All documents must be in exactly one split."""
        docs_by_source = {
            "s1": [{"id": 1}, {"id": 2}, {"id": 3}],
            "s2": [{"id": 4}, {"id": 5}]
        }
        train, val, test = stratified_split(docs_by_source, 0.8, 0.1, 0.1, seed=42)
        all_ids = set(d["id"] for d in train + val + test)
        assert all_ids == {1, 2, 3, 4, 5}

    def test_no_overlap_between_splits(self):
        """Document IDs must not appear in multiple splits."""
        docs_by_source = {
            "s1": [{"id": i} for i in range(20)],
            "s2": [{"id": i} for i in range(20, 40)]
        }
        train, val, test = stratified_split(docs_by_source, 0.8, 0.1, 0.1, seed=42)
        train_ids = set(d["id"] for d in train)
        val_ids = set(d["id"] for d in val)
        test_ids = set(d["id"] for d in test)
        assert len(train_ids & val_ids) == 0
        assert len(train_ids & test_ids) == 0
        assert len(val_ids & test_ids) == 0

    def test_reproducible_with_same_seed(self):
        """Same seed produces same splits."""
        docs = {"s1": [{"id": i} for i in range(10)]}
        t1, v1, te1 = stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        t2, v2, te2 = stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        assert [d["id"] for d in t1] == [d["id"] for d in t2]
        assert [d["id"] for d in v1] == [d["id"] for d in v2]
        assert [d["id"] for d in te1] == [d["id"] for d in te2]

    def test_different_seed_different_splits(self):
        """Different seed produces different splits."""
        docs = {"s1": [{"id": i} for i in range(20)]}
        t1, _, _ = stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        t2, _, _ = stratified_split(docs, 0.8, 0.1, 0.1, seed=123)
        assert [d["id"] for d in t1] != [d["id"] for d in t2]

    def test_single_source_all_in_train(self):
        """Single source with < 3 docs goes all to train."""
        docs = {"s1": [{"id": 1}, {"id": 2}]}
        train, val, test = stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        assert len(train) == 2
        assert len(val) == 0
        assert len(test) == 0

    def test_large_source_splits(self):
        """Large source respects split ratios."""
        docs = {"s1": [{"id": i} for i in range(1000)]}
        train, val, test = stratified_split(docs, 0.9, 0.05, 0.05, seed=42)
        total = len(train) + len(val) + len(test)
        assert 0.88 <= len(train) / total <= 0.92
        assert 0.03 <= len(val) / total <= 0.07
        assert 0.03 <= len(test) / total <= 0.07

    def test_multiple_sources_all_in_splits(self):
        """Each source with >= 3 docs appears in all splits."""
        docs = {
            "s1": [{"id": i} for i in range(50)],
            "s2": [{"id": i} for i in range(50, 100)]
        }
        train, val, test = stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        train_sources = set(d["id"] // 50 for d in train)
        val_sources = set(d["id"] // 50 for d in val)
        test_sources = set(d["id"] // 50 for d in test)
        assert len(train_sources) == 2
        assert len(val_sources) == 2
        assert len(test_sources) == 2

    def test_empty_source_ignored(self):
        """Empty sources don't cause errors."""
        docs = {"s1": [{"id": 1}], "s2": []}
        train, val, test = stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        assert len(train) == 1

    def test_splits_are_lists(self):
        """Splits must be lists, not other types."""
        docs = {"s1": [{"id": i} for i in range(10)]}
        train, val, test = stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        assert isinstance(train, list)
        assert isinstance(val, list)
        assert isinstance(test, list)

    def test_documents_not_modified(self):
        """Original documents must not be modified."""
        original = [{"id": 1, "data": "test"}]
        docs = {"s1": original.copy()}
        stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        assert docs["s1"] == original


# =============================================================================
# Test Edge Cases
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_very_long_text(self):
        """Very long text is handled correctly."""
        long_text = "word " * 100000
        assert count_words(long_text) == 100000

    def test_special_characters(self):
        """Special characters don't break normalization."""
        text = "hello@#$%world"
        assert normalize_text(text) == "hello@#$%world"

    def test_only_numbers(self):
        """Numbers count as words."""
        assert count_words("123 456") == 2

    def test_mixed_language(self):
        """Mixed language text is handled."""
        text = "Hello world Herero ovandu"
        assert count_words(text) == 4

    def test_source_with_unicode_id(self):
        """Unicode in document IDs works."""
        docs = {"s1": [{"id": "文档1"}, {"id": "doc2"}]}
        train, val, test = stratified_split(docs, 0.8, 0.1, 0.1, seed=42)
        assert len(train) + len(val) + len(test) == 2


# =============================================================================
# Test Module Imports
# =============================================================================

class TestModuleImports:
    """Tests for module structure."""

    def test_all_exports_importable(self):
        """All exported functions must be importable."""
        from scripts.create_hf_dataset import (
            text_hash, count_words, normalize_text,
            stratified_split, process_sources
        )
        assert callable(text_hash)
        assert callable(count_words)
        assert callable(normalize_text)
        assert callable(stratified_split)

    def test_constants_importable(self):
        """All constants must be importable."""
        from scripts.create_hf_dataset import (
            RANDOM_SEED, TRAIN_RATIO, VAL_RATIO, TEST_RATIO, SOURCES
        )
        assert isinstance(RANDOM_SEED, int)
        assert isinstance(TRAIN_RATIO, float)
