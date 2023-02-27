import pathlib
import json
import pandas as pd
#extracting random tweet ids - Ridhi

def extract_tweets():
    
    filename1 = pathlib.Path(__file__).parent.parent / "data" / "US_twitter_analysis_county.csv"
    filename2 = pathlib.Path(__file__).parent.parent / "data" / "US_twitter_analysis_state.csv"

    df1 = pd.read_csv(filename1)
    df2 = pd.read_csv(filename2)

    print(df1.head())
    print(df2.head())
    
    #tweet_ids_random = list(US_twitter['id'].sample(n = 1, random_state = 42))
    #with open("/content/drive/MyDrive/CS2_Project/tweet_ids_random.txt", "w") as f:
     #   for val in tweet_ids_random:
      #      f.write('{}'.format(val))
       #     f.write("\n")

def print_tweet():
    filename = pathlib.Path(__file__).parent / "tweets_hydrated.json"
    with open(filename, 'r') as f:
        tweets = json.load(f)
  
    for tweet in tweets["data"]:
        print(tweet["text"])
