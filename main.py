from src.scrapper import scrap_product_page, product_url
from src.book_parser import Parser
from src.csv_writer import write_to_csv
from src.category_parser import CategoryParser, CATEGORY_URL
from src.bookstore_parser import BookStoreParser
from pathlib import Path

OUTPUT_FILE = "product_info.csv"
BOOKSTORE_URL = "https://books.toscrape.com/index.html"
DATA_DIR = Path("./data")
CSV_DIR = DATA_DIR / "csv"


def ensure_data_folders() -> None:
    """Ensure data output folders exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(parents=True, exist_ok=True)


def fetch_and_parse_product(url: str, image_folder: Path = Path("./data/images/")) -> dict | None:
    page_content = scrap_product_page(url)
    if not page_content:
        return None
    parser = Parser(page_content, url)
    parser.download_image(image_folder)
    return parser.parse()


def append_product_info(product_info: dict | None, filename: str) -> None:
    if not product_info:
        return
    write_to_csv([product_info], filename)


def scrape_single_product(filename: str) -> None:
    product_info = fetch_and_parse_product(product_url)
    append_product_info(product_info, filename)
    if product_info:
        print(f"Product information has been written to {filename}")


def scrape_category_products(category_url: str) -> list[str]:
    category_page_content = scrap_product_page(category_url)
    if not category_page_content:
        return []
    category_parser = CategoryParser(category_page_content, category_url)
    product_urls = category_parser.get_all_articles()
    return product_urls


def scrape_category_to_csv(category_url: str, category_name: str) -> None:
    product_urls = scrape_category_products(category_url)
    for url in product_urls:
        product_info = fetch_and_parse_product(url)
        append_product_info(product_info, f"./data/csv/{category_name}.csv")

def scrape_all_categories_to_csv(first_category_url: str) -> None:
    category_page_content = scrap_product_page(first_category_url)
    if not category_page_content:
        return
    category_parser = BookStoreParser(category_page_content, first_category_url)
    categories = category_parser.get_all_categories()
    for category_name, category_url in categories:
        print(f"Scrapping category: {category_name} ({category_url})")
        scrape_category_to_csv(category_url, category_name)

def main():
    # Since the folders are hardcoded we ensure that they exists
    ensure_data_folders()
    print("Starting the scrapping process...")
    print("Scrapping a single product...")
    scrape_single_product(OUTPUT_FILE)
    print("Scrapping a category...")
    scrape_category_to_csv(CATEGORY_URL, OUTPUT_FILE)
    print("Scrapping all categories...")
    scrape_all_categories_to_csv(BOOKSTORE_URL)
    print("Scrapping completed successfully!")


if __name__ == "__main__":
    main()
