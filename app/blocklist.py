import os
import re
from typing import List, Set, Optional


def _read_file_text(path: str) -> str:
    with open(path, "r", encoding="utf8", errors="ignore") as f:
        return f.read()


def _tokenize(words: str) -> List[str]:
    return re.sub(r"[^\w]", " ", words).split()


def load_blocklist_words(path: Optional[str]) -> Set[str]:
    """
    Load a plain word blocklist file, returning a set of lowercase tokens.
    Lines are tokenized on non-word characters.
    """
    if not path:
        return set()
    if not os.path.exists(path):
        print(f"Blocklist word file not found: {path}")
        return set()
    content = _read_file_text(path)
    tokens = _tokenize(content.lower())
    return set(tokens)


def load_blocklist_regex(path: Optional[str]) -> List[re.Pattern]:
    """
    Load a regex blocklist file, one pattern per non-empty, non-comment line.
    Returns a list of compiled regex patterns.
    """
    patterns: List[re.Pattern] = []
    if not path:
        return patterns
    if not os.path.exists(path):
        print(f"Blocklist regex file not found: {path}")
        return patterns
    for line in _read_file_text(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            patterns.append(re.compile(line))
        except re.error as e:
            print(f"Invalid regex in {path}: {line} ({e})")
    return patterns