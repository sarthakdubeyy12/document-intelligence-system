"""Reusable text helpers."""

import re

# Separator hierarchy tried by the recursive splitter, from coarsest to finest:
# paragraphs, then lines, then words, then individual characters.
DEFAULT_SEPARATORS = ["\n\n", "\n", " ", ""]

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace into single spaces and strip the result."""
    return _WHITESPACE_RE.sub(" ", text).strip()


def split_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    separators: list[str] | None = None,
) -> list[str]:
    """Recursively split text into pieces no larger than ``chunk_size``.

    The text is split on the largest natural boundary that appears in it
    (paragraphs first, then lines, words, and finally characters), so chunks
    stay as semantically coherent as possible. Adjacent pieces are merged back
    together up to ``chunk_size`` with ``chunk_overlap`` characters of overlap.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    if not text:
        return []
    return _split_recursive(text, separators or DEFAULT_SEPARATORS, chunk_size, chunk_overlap)


def _split_recursive(
    text: str, separators: list[str], chunk_size: int, chunk_overlap: int
) -> list[str]:
    """Split ``text`` using the first usable separator, recursing on oversized pieces."""
    separator, remaining = _choose_separator(text, separators)
    splits = list(text) if separator == "" else text.split(separator)
    splits = [s for s in splits if s != ""]

    chunks: list[str] = []
    mergeable: list[str] = []
    for split in splits:
        if len(split) < chunk_size:
            mergeable.append(split)
            continue
        if mergeable:
            chunks.extend(_merge(mergeable, separator, chunk_size, chunk_overlap))
            mergeable = []
        if remaining:
            chunks.extend(_split_recursive(split, remaining, chunk_size, chunk_overlap))
        else:
            chunks.append(split)
    if mergeable:
        chunks.extend(_merge(mergeable, separator, chunk_size, chunk_overlap))
    return chunks


def _choose_separator(text: str, separators: list[str]) -> tuple[str, list[str]]:
    """Return the first separator present in ``text`` and the finer ones after it."""
    for index, separator in enumerate(separators):
        if separator == "" or separator in text:
            return separator, separators[index + 1 :]
    return separators[-1], []


def _merge(
    splits: list[str], separator: str, chunk_size: int, chunk_overlap: int
) -> list[str]:
    """Greedily join splits into chunks up to ``chunk_size``, keeping overlap between them."""
    sep_len = len(separator)
    chunks: list[str] = []
    window: list[str] = []
    length = 0
    for split in splits:
        addition = len(split) + (sep_len if window else 0)
        if length + addition > chunk_size and window:
            chunks.append(separator.join(window))
            # Drop leading splits until the carried-over text fits the overlap budget.
            while length > chunk_overlap and window:
                length -= len(window[0]) + (sep_len if len(window) > 1 else 0)
                window.pop(0)
        window.append(split)
        length += len(split) + (sep_len if len(window) > 1 else 0)
    if window:
        chunks.append(separator.join(window))
    return chunks
