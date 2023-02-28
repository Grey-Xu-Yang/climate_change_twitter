import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime

def clean_viz(filename):
    """
    This function loads the 

    """

    twitter = pd.read_csv("/content/drive/MyDrive/CS2_Project/twitter_archive/twitter.csv")
    # Take about one minute to load the twitter data set

    # convert date into year
    twitter_log_lat = twitter[twitter.lng.notnull() & twitter.lat.notnull()]
    US_range = (twitter_log_lat.lng >= -124.848974) & (twitter_log_lat.lng <= -66.885444) & (twitter_log_lat.lat > 24.396308) & (twitter_log_lat.lat < 49.384358)
    US_twitter = twitter_log_lat[US_range]
    US_twitter['time'] = pd.to_datetime(US_twitter['created_at'])
    US_twitter['date'] = US_twitter['time'].dt.date
    US_twitter['year'] = US_twitter['time'].dt.year

    # Load data into a Pandas DataFrame
    geo_file_path = "/sources/cb_2018_us_county_500k.shp"

    # Convert latitude and longitude values to Point objects
    geometry = [Point(xy) for xy in zip(US_twitter['lng'], US_twitter['lat'])]

    # Create a GeoDataFrame from the DataFrame and Point objects
    gdf = gpd.GeoDataFrame(US_twitter, geometry=geometry)

    # Load a shapefile of the United States that contains state and county boundaries
    us_map = gpd.read_file(geo_file_path)

    # Perform spatial join to match the latitude and longitude values to state and county boundaries
    result = gpd.sjoin(gdf, us_map, how='left', op='within')

    # Extract state and county names from the joined DataFrame and add them to the original DataFrame
    US_twitter['state_FIP'] = result['STATEFP']
    US_twitter['county_FIP'] = result['COUNTYFP']

    return US_twitter

def filter_for_visualization(scope)
    """ 
    This function groups the by time(either year or date) or scope
    Inputs:
        time: a pandas column defining the timeframe 
        scope: either state level or county level

    Returns:
        cleaned dataframe

    Authors: Grey and Jaskirat
    """

    US_twitter = clean_viz()

    grouped_df = US_twitter.groupby(["year", scope])
    # Define the aggregation functions for categorical and numerical variables
    # For categorical value, take the most frequently occured type, for the numerical value, take the average
    agg_dict = {'topic': lambda x: x.value_counts().index[0], 
                'stance': lambda x: x.value_counts().index[0], 
                'gender': lambda x: x.value_counts().index[0], 
                'aggressiveness': lambda x: x.value_counts().index[0], 
                'temperature_avg': 'mean',
                'sentiment': 'mean',
                'id': lambda x: list(x)}

    # Apply the aggregation
    result_df = grouped_df.agg(agg_dict)

    # Reset the index
    scope_df = result_df.reset_index()
    scope_df = scope_df[(scope_df['year'] != 2006) & (scope_df['year'] != 2007)]

    return scope_df