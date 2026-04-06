from src.scrapper import scrap_product_page, product_url
from src.book_parser import Parser
from src.csv_writer import write_to_csv
from src.category_parser import CategoryParser, CATEGORY_URL

def main():
    print("Starting the scrapping process...")
    page_content = scrap_product_page(product_url)
    parser = Parser(page_content, product_url)
    product_info = parser.parse()
    write_to_csv([product_info], "product_info.csv")
    print("Product information has been written to product_info.csv")
    print(f"Starting scrapping category: {CATEGORY_URL}")
    category_page_content = scrap_product_page(CATEGORY_URL)
    category_parser = CategoryParser(category_page_content, CATEGORY_URL)
    product_urls = category_parser.get_all_articles()
    print(f"Found {len(product_urls)} product URLs in the category.")
    for url in product_urls:
        print(f"Scrapping product page: {url}")
        product_page_content = scrap_product_page(url)
        product_parser = Parser(product_page_content, url)
        product_info = product_parser.parse()
        write_to_csv([product_info], "product_info.csv")
        print(f"Product information for {url} has been written to product_info.csv")

    if page_content:
        print("Scrapping completed successfully!")


if __name__ == "__main__":
    main()
