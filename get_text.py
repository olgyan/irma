import os
from typing import Literal, Iterable, Union

from . import marc_to_irbis


def is_irbis(text: Union[str, bytes]) -> bool:
    """Check if text contains IRBIS markers."""
    return all(marker in str(text) for marker in ('#', ':', '^', '*'))


def outof(
    file: Union[os.PathLike, str],
    mode: Literal['to string', 'to lines', 'to records']
) -> Union[str, Iterable[str]]:
    """
    Read file content with different parsing modes.
    Returns: str for 'to string', list[str] for 'to records', Iterable[str] for 'to lines'.
    """
    # Handle wrong type of input
    if not isinstance(file, (os.PathLike, str)):
        raise ValueError(f"Expected PathLike or str, got {type(file)}")
    
    # Handle direct IRBIS string input
    if isinstance(file, str) and is_irbis(file):
        return file

    # Define mode handlers
    MODE_HANDLERS = {
        'to string': lambda f: f.read(),
        'to lines': lambda f: f.readlines(),
        'to records': lambda f: [rec.strip('\n\r*') for rec in f.read().split('*****')]
    }

    # Execute the handler
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        return MODE_HANDLERS[mode](f)


def into(
    file: Union[os.PathLike, str],
    mode: Literal['from string', 'from lines', 'from records'],
    text: Union[str, Iterable[str]]
) -> None:
    """
    Write content to file with formatting.
    Raises: ValueError if text is empty or invalid.
    """
    # Validate input
    if not text:
        raise ValueError("Text cannot be empty")
    if not is_irbis(text):
        raise ValueError(f"Invalid IRBIS text: {str(text)[:80]}...")

    # Define mode handlers
    MODE_HANDLERS = {
        'from string': lambda f, t: f.write(t),
        'from lines': lambda f, t: f.writelines(t),
        'from records': lambda f, t: f.write('\n*****\n'.join(t) + '\n*****\n')
    }

    # Execute the handler
    with open(file, 'w', encoding='utf-8', errors='ignore') as f:
        MODE_HANDLERS[mode](f, text)
    print(f"Saved to {file}")
    
# Usage example
# # Read
# records = outof("data.txt", "to records")  # Returns list[str]
# lines = outof("data.txt", "to lines")      # Returns Iterable[str]

# # Write
# into("output.txt", "from records", ["rec1", "rec2"])