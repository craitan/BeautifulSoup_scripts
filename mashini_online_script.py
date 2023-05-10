from bs4 import BeautifulSoup
import requests
import openpyxl


def get_categories_links():
    url = "https://www.onlinemashini.bg/"
    response = requests.get(url)

    doc = BeautifulSoup(response.content, 'html.parser')

    links = doc.find_all('a', {'class': 'submenu active'})

    list_of_links = []

    for link in links:
        split_link_1 = str(link).split(' ')
        split_link_2 = str(split_link_1[3]).split('"')
        list_of_links.append('https://www.onlinemashini.bg' + str(split_link_2[1]))

    return list_of_links


def get_products_links():
    urls = get_categories_links()

    list_of_products_link = []

    for url in urls:

        if len(list_of_products_link) > 1:
            break

        response = requests.get("https://www.onlinemashini.bg/cat/22/klimatizaciq-ventilaciq-otoplenie/82/kaloriferi-elektri4eski-trifazni")
        doc = BeautifulSoup(response.content, 'html.parser')

        pages = doc.find('ul', {'class': 'pagination'})

        if pages != None:
            split_1 = str(pages).split("<a")
            split_2 = str(split_1[-1]).split('"')
            split_3 = str(split_2[1]).split("/")
            number = int(split_3[-1])

            for page in range(1, number + 1):

                if len(list_of_products_link) > 1:
                    break

                paged_url = f'{url}/{page}'
                response = requests.get(paged_url).text
                doc = BeautifulSoup(response, 'html.parser')

                for link in doc.find_all('div', {'class': 'col-8'}):
                    split_11 = str(link).split('href="/')
                    split_12 = str(split_11[1]).split('"')
                    product_link = f'https://www.onlinemashini.bg/{str(split_12[0])}'
                    list_of_products_link.append(product_link)

                    if len(list_of_products_link) > 1:
                        break
        elif pages:
            for link in doc.find_all('div', {'class': 'col-8'}):
                split_11 = str(link).split('href="/')
                split_12 = str(split_11[1]).split('"')
                product_link = f'https://www.onlinemashini.bg/{str(split_12[0])}'
                list_of_products_link.append(product_link)

                if len(list_of_products_link) > 1:
                    break

        else:
            break

    return list_of_products_link


def get_product_info():
    products = {}
    list_of_products_urls = get_products_links()

    for url in list_of_products_urls:
        response = requests.get(url)
        doc = BeautifulSoup(response.content, 'html.parser')
        name = doc.find(class_='product-name').text.strip()
        price = int(doc.find(class_='price mb-2 mt-1').text.strip('лв.'))/100

        product_info = doc.find('div', {'class': 'decs details'})
        product_characteristics = product_info.get_text(strip=True, separator="\n")

        if name not in products:
            products[name] = [f'{price:.2f}', str(product_characteristics)]

    return products


workbook = openpyxl.Workbook()

worksheet = workbook.active

worksheet['A1'] = 'Product Name'
worksheet['B1'] = 'Price'
worksheet['C1'] = 'Info'

row = 2
for product_name, data in get_product_info().items():
    worksheet.cell(row=row, column=1, value=product_name)
    worksheet.cell(row=row, column=2, value=data[0])
    worksheet.cell(row=row, column=3, value=data[1])
    row += 1


workbook.save('products.xlsx')