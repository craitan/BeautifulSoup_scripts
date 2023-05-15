import requests
from bs4 import BeautifulSoup


url = "https://www.toolstation.com/"

response = requests.get(url)
html_content = response.content

doc = BeautifulSoup(html_content, "html.parser")

owl_stage = doc.find('div', {'class': 'owl-stage'})

carousel = doc.find('div', {'class': 'suggestion-area'})

print(carousel)