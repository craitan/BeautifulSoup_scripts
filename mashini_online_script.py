from bs4 import BeautifulSoup
import requests
def get_categories_links():
    url = "https://www.onlinemashini.bg/"
    response = requests.get(url)

    doc = BeautifulSoup(response.content, 'html.parser')

    links = doc.find_all('a', {'class': 'submenu active'})

    list_of_links = []

    for link in links:
        new_link = str(link).split(' ')
        new_new_link = str(new_link[3]).split('"')
        list_of_links.append('https://www.onlinemashini.bg/'+ str(new_new_link[1]))


    return list_of_links


for x in get_categories_links():
    print(x)