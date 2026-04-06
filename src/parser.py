from bs4 import BeautifulSoup
from typing import List, Tuple, Dict

class Parser:
    def __init__(self, html_content, url):
        self.html_content = html_content
        self.url = url

    def get_data_from_inclass(self, class_name: str):
        """Get the data from the HTML content based on the class name."""
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
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
    

    def parse(self) -> Dict:
        """Get the product information from the HTML content."""
        table_data = self.get_data_from_inclass("table table-striped")
        # UPC / Product Type / Price (excl. tax) / Price (incl. tax) / Tax / Availability / Number of reviews
        product_info = {}
        if table_data:
            parsed_table = self.parse_table(table_data)
            for header, value in parsed_table:
                if header == "Availability":
                    header = "quantity_available"
                    product_info[header] = self.get_number_in_stock(value)
                if header == "Price (incl. tax)":
                    header = "price_including_tax"
                    product_info[header] = value
                elif header == "Price (excl. tax)":
                    header = "price_excluding_tax"
                    product_info[header] = value
                else:
                    product_info[header] = value
        product_info["category"] = self.get_category()
        product_info["product_page_url"] = self.url
        product_info["product_description"] = self.get_description()
        product_info["book_title"] = self.get_title()
        product_info["image_url"] = self.get_image_url()
        


        return product_info
