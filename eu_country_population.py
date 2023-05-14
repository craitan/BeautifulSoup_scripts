import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population"

response = requests.get(url)
html_content = response.content

doc = BeautifulSoup(html_content, "html.parser")

table = doc.find('tbody')

#crate a dict with the country name as key and the population as value
country_data = {}
# getting the data from the table
for row in table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >= 6:

        country_name = cells[1].text.strip()
        country_population = cells[2].text.strip()
        country_population = country_population.replace(',', '')
        country_population = int(country_population)
        # add the country name and population to the dict
        if country_name not in country_data and country_name != 'Total':
            country_data[country_name] = {'country_population': country_population}

#summ the population of all countries
eu_population = sum([country_data[country]['country_population'] for country in country_data])

#add the percentage of the population of each country in the dict
for country in country_data:
    country_population = country_data[country]['country_population']
    country_population_percentage = (country_population / eu_population) * 100
    country_data[country]['country_population_percentage'] = round(country_population_percentage, 1)

print(country_data)
