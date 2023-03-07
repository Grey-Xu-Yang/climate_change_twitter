from google.colab import drive
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
!pip install geopandas
import geopandas as gpd
from shapely.geometry import Point

drive.mount('/content/drive')
mydrive = "/content/drive/MyDrive/CS2_Project"
!ls $mydrive  #double check you have the correct path by listing the contents of that folder

### Part 1. Twitter Dataset Clean 
twitter = pd.read_csv("/content/drive/MyDrive/CS2_Project/twitter_archive/twitter.csv")
twitter_log_lat = twitter[twitter.lng.notnull() & twitter.lat.notnull()]
US_range = (twitter_log_lat.lng >= -124.848974) & (twitter_log_lat.lng <= -66.885444) & (twitter_log_lat.lat > 24.396308) & (twitter_log_lat.lat < 49.384358)
US_twitter = twitter_log_lat[US_range]
US_twitter['time'] = pd.to_datetime(US_twitter['created_at'])
US_twitter['date'] = US_twitter['time'].dt.date
US_twitter['year'] = US_twitter['time'].dt.year

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

### Part 2. FEMA Dataset
import pandas as pd
import json
from pandas import json_normalize
import requests
import re

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
                   "declarationDate", "incidentBeginDate", \
                   "fyDeclared", "incidentType", "declarationTitle",\
                   "fipsStateCode",	"fipsCountyCode"]

#Remove time to the right of date listed on declarationDate column
regex = re.compile(r"T.*")
df_disasters['declarationDate'] = df_disasters['declarationDate'].str.replace(regex, '')
df_disasters["incidentBeginDate"] = df_disasters["incidentBeginDate"].str.replace(regex, '')

#limiting to major disasters only
#df_major_disasters = df_disasters.loc[df_disasters["declarationType"] == "DR"]

#unique disaster types
print(df_disasters.incidentType.unique())
print(df_disasters.fyDeclared.unique())
print(df_disasters.declarationType.unique())
#sort by earliest date
#df_major_disasters.sort_values(by='declarationDate', ascending = True, inplace = True) 
df_disasters = df_disasters[columns_to_keep]


### Part 3. Merge the twitter data with FEMA
## Part 3.1. Merge based on both the event data and the county

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

## Part 3.2. Merge based on both the event data and the state
# Take 3 minute to run this line
# Group data by date and county
grouped_df2 = US_twitter.groupby(['date', 'state_FIP'])

# Define the aggregation functions for categorical and numerical variables
# For categorical value, take the most frequently occured type, for the numerical value, take the average
agg_dict2 = {'topic': lambda x: x.value_counts().index[0], 
            'stance': lambda x: x.value_counts().index[0], 
            'gender': lambda x: x.value_counts().index[0], 
            'aggressiveness': lambda x: x.value_counts().index[0], 
            'temperature_avg': 'mean',
            'sentiment': 'mean'}

# Apply the aggregation
result_df2 = grouped_df2.agg(agg_dict2)

# Reset the index
result_df2 = result_df2.reset_index()

# If the twitter release date falls into the range of starting date and ending date of the event,
# and we don't consider whether the twitter has the same county ID with the FEMA data 
df_disasters['declarationDate'] = pd.to_datetime(df_disasters['declarationDate']).dt.date
df_disasters['incidentBeginDate'] = pd.to_datetime(df_disasters['incidentBeginDate']).dt.date
df_disasters['incidentEndDate'] = pd.to_datetime(df_disasters['incidentEndDate']).dt.date
merged_df2 = pd.merge(df_disasters, result_df2, left_on='fipsStateCode', right_on = 'state_FIP')
filtered_df2 = merged_df2[(merged_df2['date'] >= merged_df2['incidentBeginDate']) & (merged_df2['date'] <= merged_df2['incidentEndDate'])]


###Part 4. Getting Twitter API for text data
!pip install twarc
import twarc

# Set your Twitter API credentials
consumer_key = "yCxPJWffCtcCQdqNb6ZGShglm"
consumer_secret = "ijqgx8YSaxsVG0TAQbcaQSeSTGhSMxW4VH8aQewO0H1nJxxLX6"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAN3xlQEAAAAAkV9D6etUpGV1y3rnrZoPgAhSC7w%3DKmU8RZJ9REiwP4kvS4XMryEfRq6rmPta04yQIMBBUXoUEE36wP"

# Initialize a Twarc instance with your API credentials, activate the below code if you are ready to pull.
t = twarc.Twarc(consumer_key, consumer_secret, bearer_token=bearer_token)

# Set the tweet ID(s) you want to hydrate
### IMPORTANT!!!!###
# Because we only have 500k of tweet we could use, we have to subset based on the data we have
# i.e. US_twitter_2019 has 383k of data
tweet_ids = [] # this could be access by asking US_twitter_2019['id']

# Hydrate the tweets and write the hydrated data to a file
with open("tweets.jsonl", "w") as f:
    for tweet in t.hydrate(tweet_ids):
        f.write(tweet)
        f.write("\n")

