from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin
from src.scrapper import scrap_product_page


CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"


class CategoryParser:
    def __init__(self, html_content, url):
        self.html_content = html_content
        self.url = url
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def get_data_from_inclass(self, class_name: str):
        """Get the data from the HTML content based on the class name."""
        element = self.soup.find(class_=class_name)
        return element

    def _get_all_articles(self) -> List:
        """Les livres sont dans une balise <article class="product_pod">."""
        articles = self.soup.find_all('article', class_='product_pod')
        return [article for article in articles]

    def is_last_page(self) -> bool:
        """Il faut vérifier s'il y a un lien vers la page suivante. Si il n'y en a pas, c'est que c'est la dernière page."""
        next_page_link = self.soup.find('li', class_='next')
        return next_page_link is None
    
    def get_next_page(self) -> str:
        """Il faut trouver le lien vers la page suivante et construire l'URL complète."""
        next_page_link = self.soup.find('li', class_='next')
        if next_page_link:
            relative_url = next_page_link.find('a')['href']
            return urljoin(self.url, relative_url)
        return ""
    
    def get_all_articles(self):
        """On get all the articles and extract the URLs of the products.
        On check if there is a next page, if there is, 
        we repeat the process until we reach the last page."""
        articles = self._get_all_articles()
        product_urls = []
        for article in articles:
            product_url = article.find('h3').find('a')['href']
            product_urls.append(urljoin(self.url, product_url))
        
        if not self.is_last_page():
            new_url = self.get_next_page()
            new_page_content = scrap_product_page(new_url)
            new_parser = CategoryParser(new_page_content, new_url)
            product_urls.extend(new_parser.get_all_articles())
        
        return product_urls

