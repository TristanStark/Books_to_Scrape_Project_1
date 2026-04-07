from bs4 import BeautifulSoup
from typing import List, Tuple
from urllib.parse import urljoin


class BookStoreParser:
    def __init__(self, html_content, url):
        self.html_content = html_content
        self.url = url
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def get_all_categories(self) -> List[Tuple[str, str]]:
        """Get all categories from the HTML content."""
        nav_list = self.soup.find('ul', class_='nav-list')
        if not nav_list:
            return []
        categories = nav_list.find_all('a')
        return [
            (category.text.strip(), urljoin(self.url, category['href']))
            for category in categories if "books_1" not in category['href']
        ]

    
