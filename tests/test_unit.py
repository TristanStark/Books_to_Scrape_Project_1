from src.parser import Parser
from src.scrapper import scrap_product_page, product_url
import pytest


def test_parser():
    page_content = scrap_product_page(product_url)
    parser = Parser(page_content, product_url)
    product_info = parser.parse()
    assert product_info["product_page_url"] == product_url
    assert product_info["universal_product_code"] == "2798974abc8a58a8"
    assert product_info["book_title"] == "Candide"
    assert product_info["price_including_tax"] == "£58.63"
    assert product_info["price_excluding_tax"] == "£58.63"
    assert product_info["quantity_available"] == 4
    assert product_info["image_url"] == "../../media/cache/e7/7d/e77d917c495e649216225bd47e006482.jpg"
    assert product_info["product_description"].startswith("Brought up in the household of a powerful Baron")