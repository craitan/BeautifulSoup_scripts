from bs4 import BeautifulSoup
import requests
import openpyxl
import time

start_time = time.time()


# def get_categories_links():
#     url = "https://www.onlinemashini.bg/"
#     response = requests.get(url)
#
#     doc = BeautifulSoup(response.content, 'html.parser')
#
#     links = doc.find_all('a', {'class': 'submenu active'})
#
#     list_of_links = []
#
#     for link in links:
#         split_link_1 = str(link).split(' ')
#         split_link_2 = str(split_link_1[3]).split('"')
#         list_of_links.append('https://www.onlinemashini.bg' + str(split_link_2[1]))
#
#     return list_of_links


def get_products_links():
    url = str(input())

    list_of_products_link = []

    response = requests.get(url)
    doc = BeautifulSoup(response.content, 'html.parser')

    get_pages = doc.find('ul', {'class': 'pagination'})

    if get_pages != None:
        last_page_link = get_pages.find_all('a')[-1]  # get the last <a> tag
        last_page_href = last_page_link['href']  # extract the "href" attribute
        last_page_number = int(last_page_href.split('/')[-1])  # get the last segment of the URL

        for page in range(1, last_page_number + 1):

            if len(list_of_products_link) > 2:
                break

            paged_url = f'{url}/{page}'
            response = requests.get(paged_url).text
            doc = BeautifulSoup(response, 'html.parser')

            for link in doc.find_all('div', {'class': 'col-8'}):
                split_link = ""
                if '<a class="name" href="/' in str(link):
                    split_link = str(link).split('<a class="name" href="/')[1].split('</a>')[0].split('">')[0]
                else:
                    continue

                product_link = f'https://www.onlinemashini.bg/{str(split_link)}'
                list_of_products_link.append(product_link)
                if len(list_of_products_link) > 2:
                    break
    # We check if there is paginator if its None but there are still products we loop through them and add them to the list of products
    elif get_pages == None and len(doc.find_all('div', {'class': 'col-8'})) > 0:

        for link in doc.find_all('div', {'class': 'col-8'}):
            split_11 = str(link).split('href="/')
            split_12 = str(split_11[1]).split('"')
            product_link = f'https://www.onlinemashini.bg/{str(split_12[0])}'
            list_of_products_link.append(product_link)

            if len(list_of_products_link) > 2:
                break
    else:
        pass

    return list_of_products_link


def get_product_info():
    products = {}
    list_of_products_urls = get_products_links()

    for url in list_of_products_urls:
        response = requests.get(url)
        doc = BeautifulSoup(response.content, 'html.parser')
        name = doc.find(class_='product-name').text.strip()

        if doc.find('div', class_='price mb-3 mt-3'):
            price = (doc.find(class_='price mb-3 mt-3').text.strip('лв.'))
        else:
            price = (doc.find(class_='price mb-2 mt-1').text.strip('лв.'))

        price = price.replace(',', '')
        price = int(price) / 100

        product_info = doc.find('div', {'class': 'decs details'})
        product_characteristics = product_info.get_text(strip=True, separator="\n")

        if doc.find('img', class_='b-r-4 product-main-image'):
            product_img = doc.find('img', class_='b-r-4 product-main-image')
            img_link = product_img["src"]
        else:
            img_link = 'No image'

        if name not in products:
            products[name] = [f'{price:.2f}', str(product_characteristics), img_link]

    return products


def create_xlsx_file_with_data():
    workbook = openpyxl.Workbook()

    worksheet = workbook.active

    worksheet['A1'] = 'Product Name'
    worksheet['B1'] = 'Price'
    worksheet['C1'] = 'Info'
    worksheet['D1'] = 'Product Img link'

    row = 2
    for product_name, data in get_product_info().items():
        worksheet.cell(row=row, column=1, value=product_name)
        worksheet.cell(row=row, column=2, value=data[0])
        worksheet.cell(row=row, column=3, value=data[1])
        worksheet.cell(row=row, column=4, value=data[2])

        row += 1

    workbook.save('mashini_online_bg.xlsx')


create_xlsx_file_with_data()

end_time = time.time()

print(end_time - start_time)
