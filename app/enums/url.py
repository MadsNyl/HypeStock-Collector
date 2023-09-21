from enum import Enum


class URLKey(Enum):
    MAIL = "mailto"
    BACKSLASH = "/"
    HTML = ".html"
    HTM = ".htm"
    TWITTER = "https://twitter.com"


class URLPattern(Enum):
    ID = r"\b(?!-)(?:[a-f\d]+-){2,}[a-f\d]+(?!-)\b"
    HYPHEN = r"\w+-\w+-\w"