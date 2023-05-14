import requests
from bs4 import BeautifulSoup
import csv

url = "https://bnb.bg/Statistics/StInterbankForexMarket/index.htm"

response = requests.get(url)
html_content = response.content

doc = BeautifulSoup(html_content, "html.parser")

table = doc.find('tbody')

data = []
# getting the data from the table
for row in table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >= 7:
        data.append(int(cells[7].text.strip().replace(' ', '')))

# sorting the data in descending order
data.sort(reverse=True)

# write the data in a csv file
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Volume sold'])
    writer.writerows(zip(data))

# read the data from the csv file
with open('data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    csv_data = [row for row in reader]

# check if the data in the csv file is different from the data we have if it is different write the new data
if csv_data != [['Volume sold']] + [[item] for item in data]:
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Volume sold'])
        writer.writerows([[item] for item in data])
