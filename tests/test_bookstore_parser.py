from src.bookstore_parser import BookStoreParser


BOOKSTORE_HTML = """
<html>
  <body>
    <ul class="nav-list">
      <li><a href="catalogue/category/books_1/index.html">Books</a></li>
      <li><a href="catalogue/category/books/travel_2/index.html"> Travel </a></li>
      <li><a href="catalogue/category/books/mystery_3/index.html">Mystery</a></li>
    </ul>
  </body>
</html>
"""


def test_get_all_categories_filters_books_root_and_builds_urls():
    parser = BookStoreParser(BOOKSTORE_HTML, "https://books.toscrape.com/index.html")
    assert parser.get_all_categories() == [
        (
            "Travel",
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        ),
        (
            "Mystery",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ),
    ]


def test_get_all_categories_returns_empty_when_nav_missing():
    parser = BookStoreParser("<html><body></body></html>", "https://books.toscrape.com")
    assert parser.get_all_categories() == []
