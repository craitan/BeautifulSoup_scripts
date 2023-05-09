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
        list_of_links.append('https://www.onlinemashini.bg' + str(new_new_link[1]))

    return list_of_links


def get_products_links():
    urls = get_categories_links()

    list_of_products_link = []

    for url in urls:

        if len(list_of_products_link) > 2:
            break

        response = requests.get(url)
        doc = BeautifulSoup(response.content, 'html.parser')

        pages = doc.find('ul', {'class': 'pagination'})

        split_1 = str(pages).split("<a")
        split_2 = str(split_1[-1]).split('"')
        split_3 = str(split_2[1]).split("/")
        number = int(split_3[-1])

        for page in range(1, number + 1):

            if len(list_of_products_link) > 2:
                break

            paged_url = f'{url}/{page}'
            response = requests.get(paged_url).text
            doc = BeautifulSoup(response, 'html.parser')

            for link in doc.find_all('div', {'class': 'col-8'}):
                split_11 = str(link).split('href="/')
                split_12 = str(split_11[1]).split('"')
                product_link = f'https://www.onlinemashini.bg/{str(split_12[0])}'
                list_of_products_link.append(product_link)

                if len(list_of_products_link) > 2:
                    break



    return list_of_products_link


print(get_products_links())
