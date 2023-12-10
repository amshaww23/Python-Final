import requests
import pandas as pd

def source_3():
    # API endpoints
    data_api_url = "https://api.ourworldindata.org/v1/indicators/699964.data.json"
    metadata_api_url = "https://api.ourworldindata.org/v1/indicators/699964.metadata.json"

    try:
        # Fetch data from the data API
        response_data = requests.get(data_api_url)
        data = response_data.json()

        # Convert the data to a DataFrame
        df_data = pd.DataFrame(data)

        # Fetch metadata from the metadata API
        response_metadata = requests.get(metadata_api_url)
        metadata = response_metadata.json()

        # Convert the metadata to a DataFrame
        df_metadata = pd.DataFrame(metadata['dimensions']['entities']['values'])

        # Merge data and metadata based on a common identifier ('id' for entities)
        common_column = 'id'
        df_merged = pd.merge(df_data, df_metadata, left_on='entities', right_on=common_column)

        df_merged['avg_departures'] = df_merged.groupby('name')['values'].transform('mean')
        df_avg = df_merged.groupby('name').agg({'values': 'mean', 'avg_departures': 'mean'}).reset_index()

        return df_avg

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    source_3()