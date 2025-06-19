from __future__ import annotations

from typing import List, Optional

# This is a Python reimplementation of the `seek_sequence` function from
# `seek_sequence.rs`. The goal is feature parity with the Rust version so that
# Python tools can share the same patch-parsing logic.


_DASHES = {
    "\u2010": "-",
    "\u2011": "-",
    "\u2012": "-",
    "\u2013": "-",
    "\u2014": "-",
    "\u2015": "-",
    "\u2212": "-",
}

_SINGLE_QUOTES = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201A": "'",
    "\u201B": "'",
}

_DOUBLE_QUOTES = {
    "\u201C": '"',
    "\u201D": '"',
    "\u201E": '"',
    "\u201F": '"',
}

_SPACES = {
    "\u00A0": " ",
    "\u2002": " ",
    "\u2003": " ",
    "\u2004": " ",
    "\u2005": " ",
    "\u2006": " ",
    "\u2007": " ",
    "\u2008": " ",
    "\u2009": " ",
    "\u200A": " ",
    "\u202F": " ",
    "\u205F": " ",
    "\u3000": " ",
}


def _normalise(s: str) -> str:
    table = {**_DASHES, **_SINGLE_QUOTES, **_DOUBLE_QUOTES, **_SPACES}
    return ''.join(table.get(ch, ch) for ch in s.strip())


def seek_sequence(
    lines: List[str],
    pattern: List[str],
    start: int,
    eof: bool,
) -> Optional[int]:
    """Find a subsequence within ``lines`` that matches ``pattern``.

    This function mirrors the behaviour of ``seek_sequence`` in Rust and returns
    the starting index of the match or ``None`` if not found.
    """
    if not pattern:
        return start

    if len(pattern) > len(lines):
        return None

    search_start = len(lines) - len(pattern) if eof and len(lines) >= len(pattern) else start

    # Exact match
    for i in range(search_start, len(lines) - len(pattern) + 1):
        if lines[i:i + len(pattern)] == pattern:
            return i

    # Match ignoring trailing whitespace
    for i in range(search_start, len(lines) - len(pattern) + 1):
        for p_idx, pat in enumerate(pattern):
            if lines[i + p_idx].rstrip() != pat.rstrip():
                break
        else:
            return i

    # Match ignoring leading and trailing whitespace
    for i in range(search_start, len(lines) - len(pattern) + 1):
        for p_idx, pat in enumerate(pattern):
            if lines[i + p_idx].strip() != pat.strip():
                break
        else:
            return i

    # Normalised match for fancy punctuation
    for i in range(search_start, len(lines) - len(pattern) + 1):
        for p_idx, pat in enumerate(pattern):
            if _normalise(lines[i + p_idx]) != _normalise(pat):
                break
        else:
            return i

    return None

