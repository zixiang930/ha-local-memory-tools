"""Small dependency-free relevance helpers."""

from __future__ import annotations

import re
from collections.abc import Iterable

_WORD_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


def tokenize(value: str) -> set[str]:
    """Tokenize Latin words and CJK runs for lightweight local matching."""
    return {token.casefold() for token in _WORD_RE.findall(value) if token.strip()}


def relevance(query: str, text: str, tags: Iterable[str] = ()) -> float:
    """Return a deterministic overlap score in the range 0..1."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return 0.0

    text_tokens = tokenize(text)
    tag_tokens: set[str] = set()
    for tag in tags:
        tag_tokens |= tokenize(tag)

    matched_text = len(query_tokens & text_tokens)
    matched_tags = len(query_tokens & tag_tokens)
    weighted = matched_text + (1.5 * matched_tags)
    maximum = len(query_tokens) * 1.5
    return min(1.0, weighted / maximum)
