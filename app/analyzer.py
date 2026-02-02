import re
from typing import Dict, List, Set


# Generic URL regex (not WhatsApp-specific)
URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"


def remove_urls(text: str) -> str:
    urls = re.findall(URL_REGEX, text)
    for url in urls:
        text = text.replace(url, "")
    return text


def tokenize(words: str) -> List[str]:
    return re.sub(r"[^\w]", " ", words).split()


def word_counts_from_texts(
    texts: List[str],
    min_word_length: int,
    blocklist_words: Set[str],
    blocklist_regex: List[re.Pattern],
) -> Dict[str, int]:
    """
    Compute word frequencies from a list of message texts.
    Generic processing steps:
    - Strips URLs
    - Lowercases
    - Tokenizes using word characters
    - Applies min/max length constraints
    - Filters by blocklist words and regex patterns
    Note: Any source-specific cleanup (e.g., placeholders) should be done by the respective strategy.
    """
    counts: Dict[str, int] = {}
    for msg in texts:
        if not msg:
            continue
        temp = remove_urls(msg)
        temp = temp.lower()
        words = tokenize(temp)
        for w in words:
            L = len(w)
            # enforce length constraints (45 is a sensible upper bound)
            if L < min_word_length or L > 45:
                continue
            if w in blocklist_words:
                continue
            if any(p.search(w) for p in blocklist_regex):
                continue
            counts[w] = counts.get(w, 0) + 1
    return counts