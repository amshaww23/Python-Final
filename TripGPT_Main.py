"""
but you must have at least SOME comments in each code file,
including the name of the file, the AndrewIDs of the group members,
and a description of the purpose of the code in the file,
which other module(s) import it, and which other module(s) it imports.

File Name: TripGPT_Main.py
Group Members:
    Yan Tian        yantian
    Amos Xiao       dinghuax
    Jacqueline Hsu  chiayuh
    Yiwen Cheng     yiwenc3
    Byron Chen      yilongch
Description:
TripGPT_Main builds our TripGPT algorithm based on data from 4 different sources.
The four data sources were imported as packages and merged using merge_data() function
The function get_auto_recommendation(data) is the main function to build the interactive interface between TripGPt and end users
"""

import pandas as pd
import Source1 as s1
import Source2 as s2
import Source3 as s3
import Source4 as s4

def merge_data():
    df1 = s1.source_1()
    df2 = s2.source_2()
    df3 = s3.source_3()
    df4 = s4.source_4()

    df3.rename(columns={'name': 'Country'}, inplace=True)
    merged_df = pd.merge(df1, df2, on='Country', how='inner')
    merged_df_2 = pd.merge(merged_df, df3, on='Country', how='inner')
    df = pd.merge(merged_df_2, df4, on='Country', how='inner')

    df = df.sort_values('Rank')

    df['New_Rank'] = range(1, len(df) + 1)
    df = df.drop(['Rank'], axis=1)
    df.rename(columns={'New_Rank': 'Rank'}, inplace=True)

    df = df.drop(['Advisory', 'Date Updated', 'values'], axis=1)

    df.to_csv("merged.csv", index=False)
    return df
def ask_user_questions(data):
    print("Welcome to the TripGPT!")

    while True:
        print("\nSelect an option:")
        print("-------------- TripGPT Version --------------")
        print("0. Sit back and relax! Let TripGPT do it for you!")
        print("\n----------- Manual Search Version -----------")
        print("1. Get information about a specific destination")
        print("2. Search based on Level of safety")
        print("3. Search by keywords (Beaches, mountains, museum... ")
        print("4. I'm Done!\n")

        choice = input("Enter the number of your choice: ")

        if choice == "0":
            get_auto_recommendation(data)
        elif choice == "1":
            get_destination_info(data)
        elif choice == "2":
            search_destinations(data)
        elif choice == "3":
            Keyword_destinations(data)
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def get_auto_recommendation(data):
   
    safety_df = pd.DataFrame()
    keyword_df = pd.DataFrame()
    budget_df = pd.DataFrame()

    # Filter out a dataframe that satisfy level of safety input
    while True:
        level = input("\nHow important is safety to you?\n"
                      "Rate from 1 (Super duper important!) to 4 (Hmm... I don't care that much): ")
        if level in ["1", "2", "3", "4"]:
            level = int(level)
            for level in range(1, level + 1):
                level_results = data[data['Level'].str.startswith(f'Level {level}')]
                safety_df = pd.concat([safety_df, level_results])
            break
        else:
            print("\nSorry I don't recognize this selection. Please try again.")


    # Filter out a dataframe that satisfy they keyword input
    while True:
        keywords_input = input("\nGive me one thing that excites you the MOST? ")
        keywords = [kw.strip() for kw in keywords_input.split(',')]
        keyword_df = data[data['Description'].str.contains('|'.join(keywords), case=False, regex=True)]

        if keyword_df.empty:
            print("\nSorry I could not recommend a place based on this... \n"
                  "Maybe try give me something more common? Like beach, museum, culture, etc.")
        else:
            break


    # Filter out a dataframe that satisfy travel preference, days traveling and budget input
    while True:
        travel_type = input("\nTell me about your travel preference. Are you looking for a:\n"
                            "1) Luxurious experience\n"
                            "2) Cost-Effective experience\n"
                            "3) Somewhere-in-between experience?\n")
        days = input("\nHow many days do you plan to travel? ")
        budget = input("\nWhat's your budget? ")

        days = int(days)
        budget = float(budget)

        # Use different budget group to compute the expected cost and filter on destinations
        if travel_type == '1':
            data['Expected_Cost'] = (data['High budget (tourist)'].astype(float) / 14) * days
            budget_df = data[data['Expected_Cost'] <= budget]
            break
        elif travel_type == '2':
            data['Expected_Cost'] = (data['Low budget (backpacker)'].astype(float) / 14) * days
            budget_df = data[data['Expected_Cost'] <= budget]
            break
        elif travel_type == '3':
            data['Expected_Cost'] = (data['Average budget (traveller)'].astype(float) / 14) * days
            budget_df = data[data['Expected_Cost'] <= budget]
            break
        else:
            print("Sorry I don't recognize this selection. Please try again.\n")


    # Keep only mutual rows in all three dataframes (satisfy all three criteria)
    combined_df = pd.merge(safety_df, keyword_df, on=['Destination', 'Country'])
    combined_df = pd.merge(combined_df, budget_df, on=['Destination', 'Country'])
    combined_df = combined_df.sort_values(by='Rank', ascending=True)
    combined_df['New_Rank'] = range(1, len(combined_df) + 1)

    if combined_df.empty:
         print("\nOops! No recommendations found with the current criteria.")
         refine_search = input("Would you like to refine your search? (yes/no): ").lower()
         if refine_search == 'yes':
             get_auto_recommendation(data)
         else:
             print("Thank you for using the recommendation system. Have a great day!")
             return

         combined_df = combined_df.sort_values(by='Rank', ascending=True)
         combined_df['New_Rank'] = range(1, len(combined_df) + 1)
    else:
        print("\nThank you for all the information! \n"
              "Here are my recommendations, hope you like it :)\n")
        for index, row in combined_df.iterrows():
            print(f"Rank #{row['New_Rank']}")
            print(f"Country: {row['Country']}")
            print(f"City: {row['Destination']}")
            print(f"Estimated Cost: ${str(int(row['Expected_Cost']))}")
            print(row['Level'])
            print("Description:")
            print(row['Description'])
            print("\n------------------------")
 
   

def get_destination_info(data):
    destination_name = input("Enter the name of the destination you want information about: ")
    destination_info = data[data['Destination'] == destination_name]

    if not destination_info.empty:
        print("\nDestination Information:")
        print(f"Country: {destination_info['Country'].iloc[0]}")
        print(destination_info['Level'].iloc[0])
        print(f"Avg Departures: {destination_info['avg_departures'].iloc[0]}")
        print(f"Rank: {destination_info['Rank'].iloc[0]}")

        print("\nDescription:")
        print(destination_info['Description'].iloc[0])
    else:
        print(f"No information found for {destination_name}.")

def search_destinations(data):
    print("\nSearch for destinations based on criteria:")
    level = input("Enter the preferred travel safety level (e.g. 1: safest, 4: Most Dangerous): ")

    search_results = data[data['Level'].str.startswith(f'Level {level}')]
  

    if not search_results.empty:
        print("\nHere are some results:")
        print("\n------------------------")
        
        for index, row in search_results.iterrows():
            print(f"Country: {row['Country']}")
            print(f"Destination: {row['Destination']}")
            print(row['Level'])
            print(f"Rank: {row['Rank']}")
            print("\nDescription:")
            print(row['Description'])
            print("\n------------------------")
    else:
        print("No destinations found based on the specified criteria.")

def Keyword_destinations(data):
    print("\nSearch for destinations based on criteria:")

    keywords_input = input("\nEnter keyword to search features of the Destination: ")
    keywords = [kw.strip() for kw in keywords_input.split(',')]

    # Filter destinations based on keywords in descriptions (case-insensitive)
    keyword_results = data[data['Description'].str.contains('|'.join(keywords), case=False, regex=True)]

    if not keyword_results.empty:
        print("\nDestinations matching keywords:")
        for index, row in keyword_results.iterrows():
            print(f"Country: {row['Country']}")
            print(f"Destination: {row['Destination']}")
            print("\nDescription:")
            print(row['Description'])
            print("\n------------------------")
    else:
        print("No destinations found matching the entered keywords.")


if __name__ == '__main__':
    data = merge_data()
    # Ask user questions
    ask_user_questions(data)