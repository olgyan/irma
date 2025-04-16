import re
import sys
from pathlib import Path
from typing import Dict, List, Union, Iterable

from . import marc_to_irbis
from .get_text import outof, into


def tidy_text(
    mess: str,
    *,
    enable_default_fields: bool = True,
    enable_char_capitalization: bool = True,
    enable_whitespace_cleanup: bool = True,
    enable_replacements: Union[bool, List[str]] = True,
    enable_regexes: Union[bool, List[str]] = True,
) -> str:
    """Clean and normalize text with configurable rules. Accepts strings.
    
    Args:
        mess: Input text to process
        text_is_marc: Convert from MARC before cleanup
        enable_default_fields: Add default fields before '*****'
        enable_char_capitalization: Capitalize letters after ^
        enable_whitespace_cleanup: Normalize multiple spaces
        enable_replacements: True for all, False for none, or list of specific things to replace
        enable_regexes: True for all, False for none, or list of regex IDs (e.g., ['#210', '#215'])
    """
    
    # ===== Configuration =====
    DEFAULT_FIELDS = (
        '#920: PAZK', 
        '#610: ЭБС АЙБУКС',
        '#900: ^Tl',
        '#182: ^Ab',
        '#181: ^Ai'
    )
    
    REPLACEMENTS: Dict[str, str] = {
        '&quot;': '"',
        '&amp;': '&',
        '#856: ^U': '#951: ^I'
    }
    
    # Format: (unique_id, pattern, replacement)
    TIDYING_REGEXES = [
        ('#210', re.compile(r'(?<=#210\: )\^C(.+)\^C'), r'^C\1\n#210: ^C\''),
        ('#215', re.compile(r'(?<=#215\: )\^A(\d+) с\.'), r'^A\1\''),
        ('publisher', re.compile(r'\^(.)Издательство \"(.+)\"'), r'\1\2'),
        ('company', re.compile(r'(?:ООО|АО) \"(.+)\"'), r'\1'),
        ('ebook_link', re.compile(r'(#951\: \^Ihttps\:\/\/ibooks\.ru\/bookshelf\/\d+)(?:\^Z.+$)*?'), 
         r'\1^TСсылка на документ в ЭБС Айбукс^H05^4для автор. пользователей'),
        ('cover_link', re.compile(r'(#951\: \^Ihttps\:\/\/ibooks\.ru\/resize\/w188\/images\/T\/.+)'), 
         r'\1^TОбложка^H02'),
        ('initials', re.compile(r'(.)\.(.)\.'), r'\1. \2.')
    ]

    # ===== Processing =====
    if enable_default_fields:
        mess = mess.replace('*****', '\n'.join((*DEFAULT_FIELDS, '*****')))
    
    if enable_char_capitalization:
        mess = re.sub(r'(?<=\^)([a-zа-я])', lambda m: m.group(1).upper(), mess)
    
    if enable_whitespace_cleanup:
        mess = re.sub(r' {2,}', ' ', mess)
    
    # Handle replacements
    if enable_replacements:
        replacements = (
            REPLACEMENTS.items() if enable_replacements is True 
            else [(k, REPLACEMENTS[k]) for k in enable_replacements]
        )
        for old, new in replacements:
            mess = mess.replace(old, new)
    
    # Handle regexes
    if enable_regexes:
        regexes = (
            TIDYING_REGEXES if enable_regexes is True
            else [r for r in TIDYING_REGEXES if r[0] in enable_regexes]
        )
        for _, pattern, replacement in regexes:
            mess = pattern.sub(replacement, mess)
    
    return mess


def tidy_iter(messes: Iterable [str]) -> List:
    """Clean strings in an iterable.
    Return a list for further manipulations.
    """
    return list(tidy_text(mess) for mess in messes)
        

def tidy_file(
    file: Path,
    newfile: bool = False,
) -> None:
    """Read, clean and write an IRBIS text file.
    Args:
    file - source file
    new_file - save cleaned text to a separate file if True, 
    to the same file if False
    """
    mess = outof(file, 'to string')
    order = tidy_text(mess)
    if order == mess:
        raise ValueError
    else:
        into((f'{file}_cleaned.txt' if newfile else file), 'from string', order)


if __name__ == "__main__" and len(sys.argv) > 1:
    tidy_file(sys.argv[1], newfile=True)

# Usage Examples
#     Disable all regexes but keep basic cleanup:
#     tidy_text(mess, enable_regexes=False)

#     Only apply specific replacements:
#     tidy_text(mess, enable_replacements=['&quot;'], enable_regexes=['#215'])

#     Full processing (original behavior):
#     tidy_text(mess)  # All rules enabled