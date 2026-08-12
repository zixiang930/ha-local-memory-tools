"""Small dependency-free relevance helpers."""

from __future__ import annotations

import re
from collections.abc import Iterable

_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]+", re.UNICODE)
_CJK_RE = re.compile(r"^[\u4e00-\u9fff]+$")


def tokenize(value: str) -> set[str]:
    """Tokenize Latin words and CJK runs for lightweight local matching."""
    tokens: set[str] = set()
    for token in _TOKEN_RE.findall(value):
        normalized = token.casefold()
        tokens.add(normalized)
        if _CJK_RE.fullmatch(token) and len(token) > 1:
            tokens.update(token[index : index + 2] for index in range(len(token) - 1))
    return tokens


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
