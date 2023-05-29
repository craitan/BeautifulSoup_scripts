import requests
from bs4 import BeautifulSoup

url = "https://www.acmetools.com/cordless/drills/"
response = requests.get(url)
html_content = response.content

doc = BeautifulSoup(html_content, "html.parser")

items = doc.find('div', {'class': 'product-tile'})

print(items)
for item in items:
    print(item)