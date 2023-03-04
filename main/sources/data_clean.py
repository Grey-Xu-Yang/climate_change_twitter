from google.colab import drive
import json
from pandas import json_normalize
import requests
import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import us.states
import geopandas as gpd
from shapely.geometry import Point

drive.mount('/content/drive')
mydrive = "/content/drive/MyDrive/CS2_Project"

### Part 1. Twitter Dataset Clean 
twitter = pd.read_csv("/content/drive/MyDrive/CS2_Project/twitter_archive/twitter.csv")
twitter_log_lat = twitter[twitter.lng.notnull() & twitter.lat.notnull()]
US_range = (twitter_log_lat.lng >= -124.848974) & (twitter_log_lat.lng <= -66.885444) & (twitter_log_lat.lat > 24.396308) & (twitter_log_lat.lat < 49.384358)
US_twitter = twitter_log_lat[US_range]
US_twitter['time'] = pd.to_datetime(US_twitter['created_at'])
US_twitter['date'] = US_twitter['time'].dt.date
US_twitter['year'] = US_twitter['time'].dt.year
file_path = '/content/drive/My Drive/CS2_Project/twitter_archive/US_twitter.csv'
US_twitter.to_csv(file_path, index=False) 

# Load data into a Pandas DataFrame
file_path = "/content/drive/MyDrive/CS2_Project/us_county/cb_2018_us_county_500k.shp"
# Convert latitude and longitude values to Point objects
geometry = [Point(xy) for xy in zip(US_twitter['lng'], US_twitter['lat'])]
# Create a GeoDataFrame from the DataFrame and Point objects
gdf = gpd.GeoDataFrame(US_twitter, geometry=geometry)
# Load a shapefile of the United States that contains state and county boundaries
us_map = gpd.read_file(file_path)
# Perform spatial join to match the latitude and longitude values to state and county boundaries
result = gpd.sjoin(gdf, us_map, how='left', op='within')
# Extract state and county names from the joined DataFrame and add them to the original DataFrame
US_twitter['state_FIP'] = result['STATEFP']
US_twitter['county_FIP'] = result['COUNTYFP']

fips_to_state = {state.fips: state.name for state in us.states.STATES}
US_twitter['state_name'] = US_twitter["state_FIP"].map(fips_to_state)

### Part 2. FEMA Dataset
#attributes for data reference
#https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2

#how disasters are declared
#https://www.fema.gov/disaster/how-declared

# Set the API endpoint and parameters
url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
params = {
    "declarationType": "DR",       # Limit to disasters declared as major disasters
    "state": "US",             # Limit to natural disasters in the United States
    "incidentBeginDate": "2012-02-14T00:00:00.000Z",  # Start date for data retrieval
    "limit": 1000              # Maximum number of records to retrieve
}

# Make the request
response = requests.get(url, params=params)
disaster_data = response.json()

#Convert to pandas dataframe
df_disasters = json_normalize(disaster_data["DisasterDeclarationsSummaries"])

columns_to_keep = ["disasterNumber", "state", "declarationType",\
                   "declarationDate", "incidentBeginDate","incidentEndDate", \
                   "fyDeclared", "incidentType", "declarationTitle",\
                   "fipsStateCode",	"fipsCountyCode"]

#Remove time to the right of date listed on declarationDate column
regex = re.compile(r"T.*")
df_disasters['declarationDate'] = df_disasters['declarationDate'].str.replace(regex, '')
df_disasters["incidentBeginDate"] = df_disasters["incidentBeginDate"].str.replace(regex, '')
df_disasters["incidentEndDate"] = df_disasters["incidentEndDate"].str.replace(regex, '')
df_disasters = df_disasters[columns_to_keep]

file_path = '/content/drive/My Drive/CS2_Project/twitter_archive/FEMA_disaster.csv'
df_disasters.to_csv(file_path, index=False) 

### Part 3. Merge the twitter data with FEMA
## Part 3.1. Merge based on both the event date and the county

# Take 7 minute to run this line
# Group data by date and county
grouped_df = US_twitter.groupby(['date', 'county_FIP'])

# Define the aggregation functions for categorical and numerical variables
# For categorical value, take the most frequently occured type, for the numerical value, take the average
agg_dict = {'topic': lambda x: x.value_counts().index[0], 
            'stance': lambda x: x.value_counts().index[0], 
            'gender': lambda x: x.value_counts().index[0], 
            'aggressiveness': lambda x: x.value_counts().index[0], 
            'temperature_avg': 'mean',
            'sentiment': 'mean'}

# Apply the aggregation
result_df = grouped_df.agg(agg_dict)

# Reset the index
result_df = result_df.reset_index()

# If the twitter has the same county ID with the FEMA data, and the twitter release date falls into the 
# range of starting date and ending date of the event
df_disasters['declarationDate'] = pd.to_datetime(df_disasters['declarationDate']).dt.date
df_disasters['incidentBeginDate'] = pd.to_datetime(df_disasters['incidentBeginDate']).dt.date
df_disasters['incidentEndDate'] = pd.to_datetime(df_disasters['incidentEndDate']).dt.date
merged_df = pd.merge(df_disasters, result_df, left_on='fipsCountyCode', right_on = 'county_FIP')
filtered_df = merged_df[(merged_df['date'] >= merged_df['incidentBeginDate']) & (merged_df['date'] <= merged_df['incidentEndDate'])]

## Part 3.1. Merge based on both the event date and county
# Take 7 minute to run this line
# Group data by date and county
grouped_df = US_twitter.groupby(['date', 'county_FIP'])
grouped_df_year = US_twitter.groupby(['year', 'county_FIP'])

# Define the aggregation functions for categorical and numerical variables
# For categorical value, take the most frequently occured type, for the numerical value, take the average
agg_dict = {'topic': lambda x: x.value_counts().index[0], 
            'stance': lambda x: x.value_counts().index[0], 
            'gender': lambda x: x.value_counts().index[0], 
            'aggressiveness': lambda x: x.value_counts().index[0], 
            'state_name': lambda x: x.iloc[0],
            'county_name': lambda x: x.iloc[0],
            'temperature_avg': 'mean',
            'sentiment': 'mean',
            'id': lambda x: list(x)}

# Apply the aggregation
result_df = grouped_df.agg(agg_dict)
result_df_year = grouped_df_year.agg(agg_dict)

# Reset the index
result_df = result_df.reset_index()
result_df_year = result_df_year.reset_index()
result_df_year = result_df_year.iloc[:,:-1]

df_disasters['declarationDate'] = pd.to_datetime(df_disasters['declarationDate']).dt.date
df_disasters['incidentBeginDate'] = pd.to_datetime(df_disasters['incidentBeginDate']).dt.date
df_disasters['incidentEndDate'] = pd.to_datetime(df_disasters['incidentEndDate']).dt.date
merged_df = pd.merge(df_disasters, result_df, left_on='fipsCountyCode', right_on = 'county_FIP')
filtered_df = merged_df[(merged_df['date'] >= merged_df['incidentBeginDate']) & (merged_df['date'] <= merged_df['incidentEndDate'])]

file_path = '/content/drive/My Drive/CS2_Project/twitter_archive/merged_county_only.csv'
merged_df = merged_df.iloc[:,:-1]
merged_df.to_csv(file_path, index=False) 

# There is only five events that are matched.
file_path = '/content/drive/My Drive/CS2_Project/twitter_archive/merged_date_county.csv'
filtered_df.to_csv(file_path, index=False) 

## Part 3.2. Merge based on both the event date and the state
# Take 3 minute to run this line
# Group data by date and county
grouped_df2 = US_twitter.groupby(['date', 'state_FIP'])
grouped_df2_year = US_twitter.groupby(['year', 'state_FIP'])

# Define the aggregation functions for categorical and numerical variables
# For categorical value, take the most frequently occured type, for the numerical value, take the average
agg_dict2 = {'topic': lambda x: x.value_counts().index[0], 
            'stance': lambda x: x.value_counts().index[0], 
            'gender': lambda x: x.value_counts().index[0], 
            'aggressiveness': lambda x: x.value_counts().index[0], 
            'state_name': lambda x: x.iloc[0],
            'temperature_avg': 'mean',
            'sentiment': 'mean',
             'id': lambda x: list(x)}

# Apply the aggregation
result_df2 = grouped_df2.agg(agg_dict2)
result_df2_year = grouped_df2_year.agg(agg_dict2)
# Reset the index
result_df2 = result_df2.reset_index()
result_df2_year = result_df2_year.reset_index()
result_df2_year = result_df2_year.iloc[:,:-1]

file_path = '/content/drive/My Drive/CS2_Project/twitter_archive/twitter_year_state.csv'
result_df2_year.to_csv(file_path, index=False) 

# If the twitter release date falls into the range of starting date and ending date of the event,
# and we don't consider whether the twitter has the same county ID with the FEMA data 
merged_df2 = pd.merge(df_disasters, result_df2, left_on='fipsStateCode', right_on = 'state_FIP')
filtered_df2 = merged_df2[(merged_df2['date'] >= merged_df2['incidentBeginDate']) & (merged_df2['date'] <= merged_df2['incidentEndDate'])]

file_path = '/content/drive/My Drive/CS2_Project/twitter_archive/merged_state_only.csv'
merged_df2 = merged_df2.iloc[:,:-1]
merged_df2.to_csv(file_path, index=False)

file_path = '/content/drive/My Drive/CS2_Project/twitter_archive/merged_date_state.csv'
filtered_df2.to_csv(file_path, index=False) 

