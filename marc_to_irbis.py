import re
from pathlib import Path


# Remove XML record tags and insert IRBIS delimiters
MARC_TO_IRBIS_REGEXES = [
    (re.compile(r'<record syntax="RUSMarc">'), r''),
    (re.compile(r'</record>'), r'\n*****\n'),
    (re.compile(r'<(leader|indicator).+?</\1>'), r''),
    (re.compile(r'<field id="(\d+)">'), r'\n#\1: '),
    (re.compile(r'<subfield id="(.)">'), r'^\1'),
    (re.compile(r'</(?:sub)?field>'), r''),
    (re.compile(r'^\w\s*?\n'), r''),
    (re.compile(r'\n{2,}'), r'\n')
]


def is_marc(text: str) -> bool:
    """Check if text contains IRBIS markers."""
    if text is Path:
        return bool(text.suffix == '.xml')
    else:
        return all(marker in str(text) for marker in ('<', '>', '</', 'record'))


def convert(text: str) -> str:
    """Remove XML tags and insert IRBIS delimiters with a set of regexes"""
    for pattern, replacement in MARC_TO_IRBIS_REGEXES:
        text = pattern.sub(replacement, text)
    return text
