from src.scrapper import scrap_product_page, product_url
from src.parser import Parser

def main():
    print("Starting the scrapping process...")
    page_content = scrap_product_page(product_url)
    parser = Parser(page_content, product_url)
    product_info = parser.parse()
    print("Product Information:")
    for key, value in product_info.items():
        print(f"{key}: {value}")
    if page_content:
        print("Scrapping completed successfully!")


if __name__ == "__main__":
    main()
