"""Analyze text: length, uppercase count, digits, and special characters."""

from typing import Iterable


class TextAnalyzer:
    """Analyze a string or a list of strings."""

    def __init__(self, data: str | Iterable[str]) -> None:
        """Store input. Accepts a string or an iterable of strings."""
        if isinstance(data, str):
            self._text = data
        else:
            self._text = "".join(data)

    def total_length(self) -> int:
        """Return total length of the input."""
        return len(self._text)

    def uppercase_count(self) -> int:
        """Return number of uppercase letters (A–Z)."""
        return sum(1 for ch in self._text if ch.isupper())

    def digit_count(self) -> int:
        """Return number of digits (0–9)."""
        return sum(1 for ch in self._text if ch.isdigit())

    def special_count(self, include_space: bool = False) -> int:
        """
        Return number of special characters.

        A special character is any character that is NOT alphanumeric.
        If include_space is False (default), spaces are excluded from the count.
        """
        def is_special(ch: str) -> bool:
            if not include_space and ch.isspace():
                return False
            return not ch.isalnum()

        return sum(1 for ch in self._text if is_special(ch))


if __name__ == "__main__":
    SAMPLE = "Hello, This is a sample text! It contains 2 digits: 1 and 2.\nNew line here."
    analyzer = TextAnalyzer(SAMPLE)
    print("len:", analyzer.total_length())
    print("upper:", analyzer.uppercase_count())
    print("digits:", analyzer.digit_count())
    print("special (no space):", analyzer.special_count())
    print("special (with space):", analyzer.special_count(include_space=True))
