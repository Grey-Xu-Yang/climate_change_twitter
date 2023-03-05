import pandas as pd

US_twitter = pd.read_csv("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/twitter_compressing_effort (1) (1).csv")
US_twitter['stance'] = US_twitter['stance'].replace([3, 2, 1], ['believer', 'denier', 'neutral'])
stance_df = US_twitter[(US_twitter['year'] != 2006) & (US_twitter['year'] != 2007) & (US_twitter['year'] != 2008)]
file_path = '/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/twitter_compressing_effort.csv'
stance_df.to_csv(file_path, index=False)

    
def stance_data(stance):
    dataframe = US_twitter = pd.read_csv("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/twitter_compressing_effort.csv")
    filtered_df = dataframe[dataframe["stance"] == stance]
    grouped_df = filtered_df.groupby(['year', 'state_FIP'])

    # Define the aggregation functions for categorical and numerical variables
    # For categorical value, take the most frequently occured type, for the numerical value, take the average
    agg_dict = {
                'stance': lambda x: x.value_counts().index[0], 
                'sentiment': 'mean',}

    # Apply the aggregation
    result_df = grouped_df.agg(agg_dict)

    # Reset the index
    stance_df = result_df.reset_index()
    stance_df = stance_df[(stance_df['year'] != 2006) & (stance_df['year'] != 2007) & (stance_df['year'] != 2008)]

    return stance_df





    