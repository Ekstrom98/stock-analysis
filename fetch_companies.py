import requests as r
from bs4 import BeautifulSoup
import configparser

config = configparser.ConfigParser()
config.read('.env')

indices = ['OMXS30', 'NASDAQ100']
for index in indices:
    url = config['STOCK INDICES'][index]

    # Send a GET request
    response = r.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        td_elements=soup.find_all('td', {'class':'bold left noWrap elp plusIconTd'})
        titles = [td.a['title'].replace('\xa0', ' ') for td in td_elements if td.a and 'title' in td.a.attrs]
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    # Open a file for writing
    with open(f"./companies/{index}.txt", "w") as file:
        for title in titles:
            file.write(f"{title}\n")
