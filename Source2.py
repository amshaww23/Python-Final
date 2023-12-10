import pandas as pd
import requests
from bs4 import BeautifulSoup

def source_2():
    url = "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    rows = table.findAll('tr')
    headers = rows[0].findAll('th')

    header_list = []
    for h in headers:
        header_list = header_list + h.contents

    data = []
    each_row = []
    for row in rows[1:]:
        each_row = []
        row_data = row.findAll('td')
        each_row += row_data[0].contents[0].contents
        each_row.append(row_data[1].text.strip())
        each_row.append(row_data[2].text.strip())
        data.append(each_row)

    df = pd.DataFrame(data, columns=header_list)

    pattern = r'^(.*?)(?:,| Travel Advisory)'
    df['Country'] = df['Advisory'].str.extract(pattern)
    df = df[df['Level'].str.match(r'^Level \d')]

    df.replace('Burma (Myanmar)', 'Myanmar', inplace=True)
    df.replace('North Korea (Democratic People\'s Republic of Korea)', 'North Korea', inplace=True)
    new_row_df = pd.DataFrame([['China Travel Advisory', 'Level 3: Reconsider Travel', 'June 30, 2023', 'China']],
                              columns=['Advisory', 'Level', 'Date Updated', 'Country'])
    df = pd.concat([df, new_row_df], ignore_index=True)
    # df.to_csv('Advisory Data.csv', index=False)
    df_final = df

    return df_final


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    source_2()
