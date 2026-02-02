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
    """
    Tokenize text into words and individual emojis.
    - Words: sequences of [A-Za-z0-9_] (\w)
    - Emojis: codepoints in common emoji ranges
    """
    emoji_pattern = (
        r"[\U0001F300-\U0001F5FF"  # symbols & pictographs
        r"\U0001F600-\U0001F64F"   # emoticons
        r"\U0001F680-\U0001F6FF"   # transport & map symbols
        r"\U0001F700-\U0001F77F"   # alchemical symbols
        r"\U0001F780-\U0001F7FF"   # Geometric Shapes Extended
        r"\U0001F800-\U0001F8FF"   # Supplemental Arrows-C
        r"\U0001F900-\U0001F9FF"   # Supplemental Symbols and Pictographs
        r"\U0001FA00-\U0001FA6F"   # Chess Symbols, etc.
        r"\U0001FA70-\U0001FAFF"   # Symbols and Pictographs Extended-A
        r"\U00002700-\U000027BF"   # Dingbats
        r"\U00002600-\U000026FF"   # Misc symbols
        r"]"
    )
    pattern = re.compile(rf"\w+|{emoji_pattern}")
    return pattern.findall(words)


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
    - Tokenizes into words and emojis
    - Applies min/max length constraints (emojis bypass the minimum length)
    - Filters by blocklist words and regex patterns
    Note: Any source-specific cleanup (e.g., placeholders) should be done by the respective strategy.
    """
    def is_emoji(token: str) -> bool:
        try:
            return bool(re.search(r"[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF]", token))
        except re.error:
            # Fallback if unicode ranges aren't supported
            return False

    counts: Dict[str, int] = {}
    for msg in texts:
        if not msg:
            continue
        temp = remove_urls(msg)
        temp = temp.lower()
        words = tokenize(temp)
        for w in words:
            L = len(w)
            # enforce length constraints (45 upper bound)
            if not is_emoji(w):
                if L < min_word_length or L > 45:
                    continue
            else:
                if L > 45:
                    continue
            if w in blocklist_words:
                continue
            if any(p.search(w) for p in blocklist_regex):
                continue
            counts[w] = counts.get(w, 0) + 1
    return counts
