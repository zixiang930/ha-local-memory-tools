"""Tests for dependency-free relevance ranking."""

import importlib.util
from pathlib import Path

MODULE = (
    Path(__file__).parents[1]
    / "custom_components"
    / "ha_local_memory"
    / "ranking.py"
)
spec = importlib.util.spec_from_file_location("ranking", MODULE)
ranking = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ranking)


def test_exact_overlap_scores() -> None:
    assert ranking.relevance("bedroom temperature", "bedroom temperature preference") > 0.6


def test_tags_help_relevance() -> None:
    tagged = ranking.relevance("bedroom", "keep it cool", ["bedroom"])
    untagged = ranking.relevance("bedroom", "keep it cool", [])
    assert tagged > untagged


def test_unrelated_text_is_zero() -> None:
    assert ranking.relevance("bedroom", "garage door") == 0.0


def test_chinese_tokenization_is_stable() -> None:
    assert ranking.tokenize("卧室 温度 22度")


def test_chinese_compound_text_matches_spaced_query() -> None:
    assert ranking.relevance("卧室 温度", "卧室温度22度") > 0


def test_chinese_bigrams_are_generated() -> None:
    tokens = ranking.tokenize("卧室温度")
    assert {"卧室", "室温", "温度"} <= tokens
