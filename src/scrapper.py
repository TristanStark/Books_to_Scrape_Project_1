import requests
import time
from requests import RequestException

"""
● product_page_url
● universal_ product_code (upc)
● book_title
● price_including_tax
● price_excluding_tax
● quantity_available
● product_description
● category
● review_rating
● image_u
"""


product_url = "https://books.toscrape.com/catalogue/candide_316/index.html"


def retry_scrape(fetch_fn, retries: int = 3, delay: float = 1.0):
    """Retry a page fetch operation if it fails."""
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            result = fetch_fn()
            if result:
                return result
        except RequestException as error:
            last_error = error

        if attempt < retries:
            time.sleep(delay * attempt)

    if last_error:
        print(f"Failed to fetch page after {retries} attempts. Error: {last_error}")
    return None


def scrap_product_page(product_url, retries: int = 3, timeout: int = 10):
    def _fetch():
        response = requests.get(product_url, timeout=timeout)
        if response.status_code == 200:
            #print(response.text)  # Print the HTML content of the page
            return response.text
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

    return retry_scrape(_fetch, retries=retries)
