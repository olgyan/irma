import re
import webbrowser
from os import PathLike
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from pathlib import Path
from typing import Literal

from irma import tqdm

def check_url(url: str) -> None:
    """Check if URL is accessible, print broken links."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            if response.getcode() != 200:
                print(f"Broken: {url} (Status: {response.getcode()})")
    except (HTTPError, URLError) as e:
        print(f"Broken: {url} ({str(e)})")

def urls(mode: Literal['open', 'check'], file: PathLike) -> None:
    """Extract web links from text file and either:
    - Open them in browser tabs ('open' mode), or
    - Check for dead links ('check' mode)
    """
    # Read file content
    text = Path(file).read_text(encoding='utf-8')
    
    # Improved URL regex (handles more cases)
    url_pattern = re.compile(
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/?#][-\w./?%&=:#@]*'
    )
    found_urls = url_pattern.findall(text)
    
    if not found_urls:
        print("No URLs found in file.")
        return

    # Process URLs based on mode
    for url in tqdm(found_urls, desc='Handling URLs'):
        if mode == 'open':
            webbrowser.open(url, new=2, autoraise=True)
        elif mode == 'check':
            check_url(url)

# Example usage:
# urls('open', 'links.txt')  # Opens all links in browser
# urls('check', 'links.txt') # Checks which links are broken