Books to Scrape Scraper

Scrapes product data from https://books.toscrape.com and writes CSV files, plus downloads product images.

Prerequisites
- Python 3.10+
- uv (https://github.com/astral-sh/uv)

Setup
1. `uv sync`

Run
1. `uv run python main.py`

Tests
1. `uv run pytest`

Output
- `product_info.csv` for the single product and category run
- One CSV per category (generated during the full scrape)
- Images saved under `images/`
