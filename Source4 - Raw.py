import requests
from bs4 import BeautifulSoup

# Base URL and Headers
base_url = "https://www.whereandwhen.net/budget/"
headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X '
                          '10_14_6) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/98.0.4758.80 Safari/537.36'), 'referer': base_url}

# Target countries
target_countries = [
    "Egypt", "Thailand", "Brazil"
]

# Function to format country names into URL format
def format_country_name(country):
    return country.replace(" ", "-").lower()

# Function to extract the specific budget section
def extract_specific_section(soup):
    budget_section = soup.find('div', {'id': 'package'})
    return str(budget_section) if budget_section else "Budget section not found"

# Generate URLs and extract data
for country in target_countries:
    url = base_url + format_country_name(country) + "/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"Country: {country}\n")
    print(extract_specific_section(soup))
    print("\n" + "-"*50 + "\n")
