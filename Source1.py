import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def source_1():
    # access the website and create a soup object
    url = 'https://www.tripadvisor.com/TravelersChoice-Destinations-cPopular-g1'
    header = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X'
                             '10_14_6) AppleWebKit/537.36 (KHTML,'
                             'like Gecko) Chrome/98.0.4758.80 Safari/'
                             '537.36'), 'referer': url}

    while True:
        response = requests.get(url, headers=header)
        if response.status_code == 403:
            pass
        else:
            break

    soup = BeautifulSoup(response.text, 'lxml')

    # access the div objets containing the destinations
    get_destinations = soup.findAll('div', {'class': 'gRhGj NB Na Pa PY Pn PK'})[2:]

    # create a list of the destinations
    destinations = []

    for i in range(len(get_destinations)):
        if get_destinations[i].find('div', {'class': 'biGQs _P fiohW eIegw'}) is not None:  # accounts for 'dubai' which has a different class
            destinations.append(get_destinations[i].find('div', {'class': 'biGQs _P fiohW eIegw'}).text)
        else:
            destinations.append(get_destinations[i].find('div', {'class': 'biGQs _P fiohW rRtyp'}).text)

    # create a list of the descriptions
    descriptions = []

    for i in range(len(get_destinations)):
        desc_temp = get_destinations[i].find('span', {'class': 'JguWG'}).text.strip()
        if desc_temp.find('\n') != -1:  # concat descriptions that are split into more than one line
            desc_temp = desc_temp[:desc_temp.find('\n')] + ' ' + desc_temp[desc_temp.find('\n') + 1:]

        descriptions.append(desc_temp)

    # create a list of the country of each destination
    countries = [
        'United Arab Emirates', 'Indonesia', 'United Kingdom', 'Italy', 'France',
        'Mexico', 'Greece', 'Morocco', 'Dominican Republic', 'Turkey',
        'Mexico', 'Spain', 'India', 'Egypt', 'Spain', 'Thailand', 'Vietnam',
        'Egypt', 'Italy', 'Portugal', 'United Kingdom', 'Thailand', 'United States',
        'Qatar', 'Brazil']

    # merge data into a dataframe and write to csv
    df = pd.DataFrame({'Rank': range(1, len(destinations) + 1), 'Destination': destinations, 'Country': countries,
                       'Description': descriptions})
    # fout = open('source1.csv', 'w')
    # df.to_csv(fout, index=False)
    # close the file
    # fout.close()

    return df


if __name__ == '__main__':
    source_1()
