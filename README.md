# TripGPT

TripGPT is a personalized recommendation GUI engine, analyze user preferred activities to generate destination suggestions. Hosts interactive forums where users can ask questions, seek advice, and can have access to genuine reviews from diverse community of travelers. 

Table of Content
1.Core Functions
2.Prerequisites
3.Installation
4.Contributors:

## Core Functions:

### Source1.py

Source 1 is TripAdvisor's 25 "Best of the Best Destinations" in the world ranked. We are scraping its HTML code to retrieve the names and descriptions of each destination, then using NLP to extract the most common keywords for further analysis.

### Source2.py

Source2 of the project retrieves safety and security conditions ratings data provided by the United States Department of State from Trvel.State.Gov web page. It also visually demonstrated the safety levels of each country on a colored world map.

### Source3.py

Source3 of the project involves acquiring two API keys, consolidating two interfaces into a single metadata set, and examining the correlation between GDP and outbound data for each country.

### Source4.py

Source4.py of the project focusing on analyzing and visualizing travel budget data into structured formats include categorizing expenses like hotels, restaurants, transportation, activities for different travel styles according to different budgets for various countries. 

### TripGPT_Main.py

TripGPT_Main builds our TripGPT algorithm based on data from 4 different sources.
The four data sources were imported as packages and merged using merge_data() function
The function get_auto_recommendation(data) is the main function to build the interactive interface between TripGPt and end users
The manual search options provides user the availability to search based on one of the criteria and get recommendations.

## Prerequisites

  1. Python 3.x environment 
  2. Packages: requests, pandas, numpy, bs4, matplotlib.pyplot

## Installation
To run TripGPT, please ensure the following packages are installed:

1. `requests`: For making HTTP requests to external services.
2. `pandas`: For data manipulation and analysis.
3. `numpy`: For numerical computations.
4. `beautifulsoup4 (bs4)`: For parsing HTML and XML documents.
5. `matplotlib`: For creating static, interactive, and animated visualizations in Python.

Use the following commands to install the required packages:

```
pip install requests
pip install pandas
pip install numpy
pip install beautifulsoup4
pip install matplotlib
```

## Contributors:
Yan Tian, yantian;
Amos Xiao, dinghuax;
Jacqueline Hsu, chiayuh;
Yiwen Cheng, yiwenc3;
Byron Chen, yilongch;
