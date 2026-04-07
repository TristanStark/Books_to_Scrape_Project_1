import csv
from pathlib import Path

import pytest

from src.book_parser import Parser
from src.category_parser import CategoryParser
from src.csv_writer import write_to_csv
from src.scrapper import scrap_product_page


BOOK_HTML = """
<html>
  <body>
    <ul class="breadcrumb">
      <li><a>Home</a></li>
      <li><a>Books</a></li>
      <li><a>Fiction</a></li>
    </ul>
    <div class="product_main">
      <h1>My Book</h1>
      <p class="star-rating Three">Three</p>
    </div>
    <div class="item active">
      <img src="image.jpg" />
    </div>
    <table class="table table-striped">
      <tr><th>UPC</th><td>ABC123</td></tr>
      <tr><th>Price (incl. tax)</th><td>GBP\u00c2 10.00</td></tr>
      <tr><th>Price (excl. tax)</th><td>GBP\u00c2 9.00</td></tr>
      <tr><th>Availability</th><td>In stock (5 available)</td></tr>
    </table>
    <div id="product_description"></div>
    <p>Short description here.</p>
  </body>
</html>
"""


BOOK_HTML_MISSING = """
<html>
  <body>
    <div class="product_main"></div>
    <div class="item active"></div>
    <table class="table table-striped"></table>
  </body>
</html>
"""


PAGE_1_HTML = """
<html><body>
  <article class="product_pod">
    <h3><a href="../../../book_1/index.html">Book 1</a></h3>
  </article>
  <article class="product_pod">
    <h3><a href="../../../book_2/index.html">Book 2</a></h3>
  </article>
  <li class="next"><a href="page-2.html">next</a></li>
</body></html>
"""


PAGE_2_HTML = """
<html><body>
  <article class="product_pod">
    <h3><a href="../../../book_3/index.html">Book 3</a></h3>
  </article>
</body></html>
"""


def _parser_with_soup(html: str) -> Parser:
    parser = Parser(html, "https://example.test/book")
    parser.get_data_from_inclass("table table-striped")
    return parser


def test_parse_table_empty_returns_empty():
    parser = _parser_with_soup(BOOK_HTML)
    assert parser.parse_table(None) == []


def test_get_number_in_stock_parses_value():
    parser = _parser_with_soup(BOOK_HTML)
    assert parser.get_number_in_stock("In stock (12 available)") == 12
    assert parser.get_number_in_stock("In stock (no available)") == 0


def test_get_description_missing_returns_empty():
    parser = _parser_with_soup(BOOK_HTML_MISSING)
    assert parser.get_description() == ""


def test_get_title_missing_returns_empty():
    parser = _parser_with_soup(BOOK_HTML_MISSING)
    assert parser.get_title() == ""


def test_get_image_url_missing_returns_empty():
    parser = _parser_with_soup(BOOK_HTML_MISSING)
    assert parser.get_image_url() == ""


def test_get_category_missing_returns_empty():
    parser = _parser_with_soup(BOOK_HTML_MISSING)
    assert parser.get_category() == ""


def test_get_review_rating_missing_returns_empty():
    parser = _parser_with_soup(BOOK_HTML_MISSING)
    assert parser.get_review_rating() == ""


def test_get_price_including_tax_strips_bad_prefix():
    parser = _parser_with_soup(BOOK_HTML)
    table = parser.get_data_from_inclass("table table-striped")
    parsed_table = parser.parse_table(table)
    assert parser.get_price_including_tax(parsed_table) == "GBP 10.00"


def test_get_price_excluding_tax_strips_bad_prefix():
    parser = _parser_with_soup(BOOK_HTML)
    table = parser.get_data_from_inclass("table table-striped")
    parsed_table = parser.parse_table(table)
    assert parser.get_price_excluding_tax(parsed_table) == "GBP 9.00"


def test_parse_returns_expected_fields():
    parser = Parser(BOOK_HTML, "https://example.test/book")
    product_info = parser.parse()
    assert product_info["product_page_url"] == "https://example.test/book"
    assert product_info["universal_product_code"] == "ABC123"
    assert product_info["book_title"] == "My Book"
    assert product_info["price_including_tax"] == "GBP 10.00"
    assert product_info["price_excluding_tax"] == "GBP 9.00"
    assert product_info["quantity_available"] == 5
    assert product_info["product_description"] == "Short description here."
    assert product_info["category"] == "Fiction"
    assert product_info["review_rating"] == "Three"
    assert product_info["image_url"] == "image.jpg"


def test_category_parser_is_last_page_true_when_no_next():
    parser = CategoryParser(PAGE_2_HTML, "https://example.test/page-2.html")
    assert parser.is_last_page() is True


def test_category_parser_get_next_page_builds_url():
    url = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
    parser = CategoryParser(PAGE_1_HTML, url)
    assert (
        parser.get_next_page()
        == "https://books.toscrape.com/catalogue/category/books/fiction_10/page-2.html"
    )


def test_category_parser_get_all_articles_paginates(monkeypatch):
    def fake_scrap_product_page(url: str) -> str:
        assert url.endswith("/fiction_10/page-2.html")
        return PAGE_2_HTML

    monkeypatch.setattr("src.category_parser.scrap_product_page", fake_scrap_product_page)
    url = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
    parser = CategoryParser(PAGE_1_HTML, url)

    urls = parser.get_all_articles()
    assert urls == [
        "https://books.toscrape.com/catalogue/book_1/index.html",
        "https://books.toscrape.com/catalogue/book_2/index.html",
        "https://books.toscrape.com/catalogue/book_3/index.html",
    ]


def test_write_to_csv_creates_file_with_header_and_rows(tmp_path: Path):
    csv_path = tmp_path / "output.csv"
    data = [
        {"col1": "a", "col2": "b"},
        {"col1": "c", "col2": "d"},
    ]

    write_to_csv(data, str(csv_path))

    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))

    assert rows[0] == ["col1", "col2"]
    assert rows[1:] == [["a", "b"], ["c", "d"]]


def test_write_to_csv_appends_without_duplicate_header(tmp_path: Path):
    csv_path = tmp_path / "output.csv"
    write_to_csv([{"col1": "a", "col2": "b"}], str(csv_path))
    write_to_csv([{"col1": "c", "col2": "d"}], str(csv_path))

    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))

    assert rows == [["col1", "col2"], ["a", "b"], ["c", "d"]]


def test_write_to_csv_no_data_does_not_create_file(tmp_path: Path):
    csv_path = tmp_path / "output.csv"
    write_to_csv([], str(csv_path))
    assert csv_path.exists() is False


def test_scrap_product_page_returns_text_on_success(monkeypatch):
    class DummyResponse:
        status_code = 200
        text = "<html>ok</html>"

    def fake_get(url: str):
        assert url == "https://example.test/page"
        return DummyResponse()

    monkeypatch.setattr("src.scrapper.requests.get", fake_get)
    assert scrap_product_page("https://example.test/page") == "<html>ok</html>"


def test_scrap_product_page_prints_error_on_failure(monkeypatch, capsys):
    class DummyResponse:
        status_code = 404
        text = ""

    def fake_get(url: str):
        return DummyResponse()

    monkeypatch.setattr("src.scrapper.requests.get", fake_get)
    assert scrap_product_page("https://example.test/page") is None
    captured = capsys.readouterr()
    assert "Failed to fetch the page. Status code: 404" in captured.out
