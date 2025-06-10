import requests
import webbrowser
from bs4 import BeautifulSoup
from collections import namedtuple
from os import PathLike
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from typing import Literal
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

from irma import get_text
from irma import tqdm
from irma.python_url_regex import NET_ADDR_PATTERN as URL_PATTERN


def check(url: str) -> None:
    """Check if URL is accessible, print broken links."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            if response.getcode() != 200:
                print(f"Broken: {url} (Status: {response.getcode()})")
    except (HTTPError, URLError) as e:
        print(f"Broken: {url} ({str(e)})")


def open_in_browser(url: str) -> None:
    webbrowser.open(url, new=2, autoraise=True)


def extract_from(file: PathLike | str) -> list:
    """Extract web links from text file."""
    # Read file content
    try:
        text = Path(file).read_text(encoding='utf-8', errors='ignore')
    except FileNotFoundError:
        text = file

    # Find URLs with regex
    found_urls = URL_PATTERN.findall(text)
    if not found_urls:
        print("No URLs found in file.")
        return
    return found_urls


def selenium_scrape(urls, results=[]):
    """Properly maintained driver instance for multiple URLs"""
    # Initialize driver with persistent settings
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    options.add_argument("-headless")
    
    # Start driver (will persist for all URLs)
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)  # Global timeout
    
    try:
        for url in tqdm(urls):
            try:
                driver.get(url)  # Always start fresh
                
                # Reset execution context
                WebDriverWait(driver, 15).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                
                # Multiple ways to detect the "Read" button
                read_button_selectors = [
                    ("CSS", "ebs-book-read-button button.button-read"),  # Component structure
                    ("XPATH", "//button[contains(@class,'button-read') and contains(.,'Читать')]"),
                    ("CSS", "button.mat-raised-button:has(span:contains('Читать'))"),  # Material button
                    ("XPATH", "//ebs-book-read-button//button[span[contains(text(),'Читать')]]")
                ]
                
                result = {
                    "url": url,
                    "has_read_link": False,
                }
                
                # Check for read button
                for by, selector in read_button_selectors:
                    try:
                        btn = driver.find_element(
                            (By.CSS_SELECTOR if by == "CSS" else By.XPATH), selector)
                        if btn.is_displayed():
                            result["has_read_link"] = True
                            break
                    except:
                        continue
                
            except Exception as e:
                driver.save_screenshot(f"error_{url.split('/')[-1]}.png")
                print(f"Error checking {url}: {str(e)}")
                result["has_read_link"] = None
            
            finally:
                results.append(result)
        
    finally:
        # Ensure driver quits even if errors occur
        driver.quit()
        return results


def check_page(session, url):
    """Check a single page for the required elements"""
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if 'znanium' in url:
        # Check for "Читать книгу" link
        read_link = soup.find('a', string='Читать книгу') or \
                    soup.find('span', {'class': 'hover_title'}, string='Читать книгу')
  
    elif 'ibooks' in url:
        read_link = soup.find('a', {'class': 'btn btn--small'})

    return read_link is not None


def scrape(urls):
    """Main scraping function"""
    session = requests.Session()
        # Set headers to mimic a browser
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64;'
                            ' x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/91.0.4472.124 Safari/537.36'})
    
    results = []
    lanbook_urls = [] # collect them to treat them separately
    for url in urls:
        try:
            if 'lanbook' in url:
                lanbook_urls.append(url)
                continue
            else:
                result = check_page(session, url)
                results.append({'url': url, 'has_read_link': result})

        except Exception as e:
            print(f'Error checking {url}: {str(e)}')
            results.append({'url': url, 'has_read_link': None})

    if lanbook_urls:
        print("Launching browser to render JavaScript from e.lanbook.com...")
        selenium_scrape(lanbook_urls, results)

    # Handling results
    unavailables = [res['url'] for res in results if not res['has_read_link']]
    print(f'{len(unavailables)}'
        f' unavailable books out of {len(urls)} books found.')

    # return results
    return unavailables

def get_book_info(putlog_filename, book_args):
    Book = namedtuple('Book', book_args)
    f = get_text.outof(putlog_filename, 'lines')
    books = [Book(*elem) for elem in f] # type: ignore
    # urls = set(book.url for book in books)
    return books

if __name__ == '__main__':
    # pass
    get_text.process_and_save(scrape, r'c:\irbiswrk\znanium_links_2025.txt', 'lines')
