import requests

"""
● product_page_url
● universal_ product_code (upc)
● book_title
● price_including_tax
● price_excluding_tax
● quantity_available
● product_description
● category
● review_rating
● image_u
"""


product_url = "https://books.toscrape.com/catalogue/candide_316/index.html"


def scrap_product_page(product_url):
    response = requests.get(product_url)
    if response.status_code == 200:
        print("Page fetched successfully!")
        #print(response.text)  # Print the HTML content of the page
        return response.text
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")