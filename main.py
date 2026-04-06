from src.scrapper import scrap_product_page, product_url
from src.parser import Parser
from src.csv_writer import write_to_csv

def main():
    print("Starting the scrapping process...")
    page_content = scrap_product_page(product_url)
    parser = Parser(page_content, product_url)
    product_info = parser.parse()
    write_to_csv([product_info], "product_info.csv")


    if page_content:
        print("Scrapping completed successfully!")


if __name__ == "__main__":
    main()
