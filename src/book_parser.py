from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
from pathlib import Path
from urllib.parse import urljoin
import requests


class Parser:
    def __init__(self, html_content, url):
        self.html_content = html_content
        self.url = url
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def get_data_from_inclass(self, class_name: str):
        """Get the data from the HTML content based on the class name."""
        element = self.soup.find(class_=class_name)
        return element

    def parse_table(self, table) -> List[Tuple[str, str]]:
        """Parse the table"""
        results: List[Tuple[str, str]] = []
        if table:
            rows = table.find_all('tr')
            for row in rows:
                header = row.find('th').text.strip()
                value = row.find('td').text.strip()
                results.append((header, value))
        return results

    def get_category(self) -> str:
        """La catégorie est dans le breadcrumb, il faut trouver le lien qui correspond à la catégorie et extraire le texte."""
        breadcrumb = self.soup.find('ul', class_='breadcrumb')
        if breadcrumb:
            # 0 => Home
            # 1 => Books
            category_link = breadcrumb.find_all('li')[2].find('a')
            if category_link:
                return category_link.text.strip()
        return ""

    def get_number_in_stock(self, availability: str) -> int:
        """Extract the number of items in stock from the availability string."""
        import re
        match = re.search(r'(\d+) available', availability)
        if match:
            return int(match.group(1))
        return 0

    def get_description(self) -> str:
        """Get the product description from the HTML content."""
        description_element = self.soup.find('div', id="product_description")
        if description_element:
            description = description_element.find_next_sibling('p')
            if description:
                return description.text.strip()
        return ""
    
    def get_title(self) -> str:
        """Get the book title from the HTML content."""
        title_element = self.soup.find('div', class_='product_main').find('h1')
        if title_element:
            return title_element.text.strip()
        return ""
    
    def get_image_url(self) -> str:
        """Get the image URL from the HTML content."""
        image_element = self.soup.find('div', class_='item active').find('img')
        if image_element:
            return image_element['src']
        return ""
    

    def get_availability(self, parsed_table) -> str:
        """Get the availability from the parsed table."""
        for header, value in parsed_table:
            if header == "Availability":
                return self.get_number_in_stock(value)
        return ""

    def get_upc(self, parsed_table) -> str:
        """Get the UPC from the parsed table."""
        for header, value in parsed_table:
            if header == "UPC":
                return value
        return ""
    
    def get_price_including_tax(self, parsed_table) -> str:
        """Get the price including tax from the parsed table."""
        for header, value in parsed_table:
            if header == "Price (incl. tax)":
                return value.replace("Â", "")
        return ""

    def get_price_excluding_tax(self, parsed_table) -> str:
        """Get the price excluding tax from the parsed table."""
        for header, value in parsed_table:
            if header == "Price (excl. tax)":
                return value.replace("Â", "")
        return ""
    
    def get_review_rating(self) -> str:
        """Get the review rating from the HTML content."""
        rating_element = self.soup.find('p', class_='star-rating')
        if rating_element:
            classes = rating_element['class']
            for cls in classes:
                if cls != 'star-rating':
                    return cls
        return ""

    def parse(self) -> Dict:
        """Get the product information from the HTML content."""
        table_data = self.get_data_from_inclass("table table-striped")
        # UPC / Product Type / Price (excl. tax) / Price (incl. tax) / Tax / Availability / Number of reviews
        product_info = {}
        parsed_table = self.parse_table(table_data)
        product_info["product_page_url"] = self.url
        product_info["universal_product_code"] = self.get_upc(parsed_table)
        product_info["book_title"] = self.get_title()
        product_info["price_including_tax"] = self.get_price_including_tax(parsed_table)
        product_info["price_excluding_tax"] = self.get_price_excluding_tax(parsed_table)
        product_info["quantity_available"] = self.get_availability(parsed_table)
        product_info["product_description"] = self.get_description()
        product_info["category"] = self.get_category()
        product_info["review_rating"] = self.get_review_rating()
        product_info["image_url"] = self.get_image_url()

        return product_info


    def download_image(self, folder: Path) -> str:
        """Download the image """
        image_url = self.get_image_url()
        if not image_url:
            return ""
        absolute_image_url = urljoin(self.url, image_url)
        # Download the image and save it to the specified folder
        response = requests.get(absolute_image_url)
        if response.status_code == 200:
            folder.mkdir(parents=True, exist_ok=True)
            image_name = f"{self.get_title()}.jpg"
            # We normalize the image name to avoid issues with special characters in file names
            image_name = "".join(c for c in image_name if c.isalnum() or c in (' ', '.', '_')).rstrip()
            image_path = folder / image_name
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return str(image_path)
        return ""
