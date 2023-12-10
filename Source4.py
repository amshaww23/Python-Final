"""
File Name: Source4.py
Group Members:
    Yan Tian        yantian
    Amos Xiao       dinghuax
    Jacqueline Hsu  chiayuh
    Yiwen Cheng     yiwenc3
    Byron Chen      yilongch
Description:
Source4.py is an integral part of the TripGPT project, focusing on analyzing and visualizing 
travel budget data for various countries. 

##1.Data Scraping and Parsing: 
This Script retives data from "https://www.whereandwhen.net/budget/" for a predefined list of countries. 
It parses this data to extract detailed information about travel expenses 
across categories such as hotels, restaurants, transportation, and activities.

##2.Budget Information Extract:
Using BeautifulSoup for HTMP parsing and organize budget data into structed formats include 
categorizing expenses for different travel styles(low, average, high budeget)

##3.Data Visualiztion:
Using Matplotlib created several bar plots represent travel expenses in the aforementioned actegories
for different countries
"""
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

# Base URL and Headers
base_url = "https://www.whereandwhen.net/budget/"
headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X '
                          '10_14_6) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/98.0.4758.80 Safari/537.36'), 'referer': base_url}

# List of target countries for which the budget data is to be scraped
target_countries = [
    "United Arab Emirates", "Indonesia", "Italy", "France", "Greece", 
    "Morocco", "Dominican Republic", "Turkey", "Spain", "India", 
    "Egypt", "Thailand", "Brazil"
]

# Function to format country names into URL format
def format_country_name(country):
    return country.replace(" ", "-").lower()

# Function to extract and parse budget information
def extract_and_parse_budget_info(soup):
    budget_info = {}
    # Finding all div elements that contain budget information
    budget_divs = soup.find_all('div', class_='col-sm-4')

    for div in budget_divs:
        # Extracting the budget type (e.g., low, average, high)
        h4 = div.find('h4')
        if h4:
            budget_type = h4.text.strip()
            # Initializing
            expenses = {"Hotel": 0.0, "Restaurant": 0.0, "Transportation": 0.0, "Activities": 0.0}
            category_index = 0
            category_names = ["Hotel", "Restaurant", "Transportation", "Activities"]
            
            # Parsing each expense listed under the budget type
            for li in div.find_all('li'):
                text = li.get_text().strip()
                try:
                    # Extracting and calculating the expense value
                    if 'for 2 ppl.' in text:
                        value = float(text.split('$')[1].split(' for')[0])
                        expense_value = value * 2
                    elif 'per person' in text:
                        value = float(text.split('$')[1].split(' per')[0])
                        expense_value = value
                    elif 'Free activities' in text:
                        expense_value = 0.0
                    else:
                        continue
                    
                    # Assigning the expense value to the correct category
                    if category_index < len(category_names):
                        expenses[category_names[category_index]] = expense_value
                        category_index += 1
                except ValueError as e:
                    print(f"Error parsing expenses: {e}")
                    
            # Extracting the total budget for the budget type
            total_budget_p = div.find('p', class_='prix')
            if total_budget_p:
                try:
                    total_budget_text = ''.join(filter(lambda x: x.isdigit() or x == '.', total_budget_p.get_text().split('$')[1].split('*')[0]))
                    total_budget = float(total_budget_text)
                except ValueError as e:
                    print(f"Error parsing total budget: {e}")
                    total_budget = 0.0
            else:
                total_budget = 0.0
                
            # Storing the parsed data in the budget_info dictionary
            budget_info[budget_type] = {
                "Expenses": expenses,
                "Total Budget": total_budget
            }

    return budget_info


# Function to plot the data
def plot_budget_data(data):
    # Getting the list of countries from the data
    countries = list(data.keys())
    # Defining the categories for expenses
    expense_categories = ['Hotel', 'Restaurant', 'Transportation', 'Activities', 'Total']
    
    # Iterating over each expense category to create a plot
    for category in expense_categories:
        fig, ax = plt.subplots(figsize=(12, 6))

        # Bar settings
        bar_width = 0.2
        opacity = 0.8
        index = np.arange(len(countries))

        if category == 'Total':
            # Collecting total budget data for each budget type
            low_budgets = [data[country].get('Low budget (backpacker)', {}).get('Total Budget', 0) for country in countries]
            avg_budgets = [data[country].get('Average budget (traveller)', {}).get('Total Budget', 0) for country in countries]
            high_budgets = [data[country].get('High budget (tourist)', {}).get('Total Budget', 0) for country in countries]
        else:
            # Collecting data for each budget type and expense category
            low_budgets = [data[country].get('Low budget (backpacker)', {}).get('Expenses', {}).get(category, 0) for country in countries]
            avg_budgets = [data[country].get('Average budget (traveller)', {}).get('Expenses', {}).get(category, 0) for country in countries]
            high_budgets = [data[country].get('High budget (tourist)', {}).get('Expenses', {}).get(category, 0) for country in countries]

        # Plotting the bars
        ax.bar(index, low_budgets, bar_width, alpha=opacity, label='Low Budget')
        ax.bar(index + bar_width, avg_budgets, bar_width, alpha=opacity, label='Average Budget')
        ax.bar(index + 2*bar_width, high_budgets, bar_width, alpha=opacity, label='High Budget')

        # Setting the labels and titles
        ax.set_xlabel('Country')
        ax.set_ylabel(f'{category} Costs ($)' if category != 'Total' else 'Total Budget ($)')
        ax.set_title(f'{category} Costs by Country and Budget Level' if category != 'Total' else 'Total Budget by Country and Budget Level')
        ax.set_xticks(index + bar_width)
        ax.set_xticklabels(countries)
        ax.legend()

        # Rotate the x-axis labels to prevent overlap
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()





# Main function to run the program
def main():
    all_data = {}
    # Iterating over each target country to scrape and parse data
    for country in target_countries:
        url = base_url + format_country_name(country) + "/"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracting and parsing budget information for each country
        budget_info = extract_and_parse_budget_info(soup)
        all_data[country] = budget_info

        # Print the budget information for the country
        print(f"Budget information for {country}:")
        for budget_type, info in budget_info.items():
            print(f"  {budget_type}:")
            for key, value in info.items():
                print(f"    {key}: {value}")
        print("\n")  # Add a newline for better readability

    # Plot the data
    plot_budget_data(all_data)

# Executing the main function
main()

