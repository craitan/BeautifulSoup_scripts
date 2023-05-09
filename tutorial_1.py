from bs4 import BeautifulSoup
import requests

url = "https://www.mashini.bg/akumulatorni-kosachki"

page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

# Empty dictionary that we are going to add the names and the price of the products
products = {}

# The number of pages for each product
pages = int(doc.find(class_='page-link').text)

# Loop through the products pages.
for page in range(1, pages + 1):
    # Here we create new url with the page number
    url = f'https://www.mashini.bg/akumulatorni-kosachki?page={page}&orderby=default'

    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    # Here we add the products names to a list so we can use it latter.
    products_name = []

    # While looping we get the products names and add them to the products_name list.
    for h3 in doc.find_all('h3', {'class': 'name'}):
        title = h3.text.strip()
        products_name.append(title)

    # While looping we get the products prices.
    product_new_price = doc.find_all('span', {'class': 'price-new'})

    # If we need the old price of the products.
    """product_old_price = doc.find_all('span', {'class': 'price-old'})"""

    # We add the products in the dictionary with value empty list in which we will add the price and more information
    for name in products_name:
        if name not in products:
            products[name] = []

    # Here we add the price of the products.
    for i, new_price in enumerate(product_new_price):
        name = products_name[i]
        products[name].append(new_price.text)

# # We have to work on this if we need the old prices.
# for i, old_price in enumerate(product_old_price):
#     name = product_name[i].text
#     products[name].append(old_price.text)
#

# print the product name and price
for product, prices in products.items():
    print(f"Product: {product} -- Price: {prices[0]}")

print(len(products))
# 1. Will check latter how to crate CSV file and add the data.
# 2. Will try to open every product and get the specific info that we need.
