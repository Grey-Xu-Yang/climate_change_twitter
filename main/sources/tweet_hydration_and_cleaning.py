import pathlib
import json
import pandas as pd
import numpy as np
#extracting random tweet ids - Ridhi Purohit

def extract_tweet_ids():
    '''
    
    '''
    filename1 = pathlib.Path(__file__).parent.parent / "data" / "US_twitter_analysis_county.csv"

    df1 = pd.read_csv(filename1)
    
    id_contain = []
    for item in df1['id']:
        my_list = item.split(",")
        for val in my_list:
            id_contain.append(val)

    ids = pd.Series(id_contain)
    tweet_ids_random = list(ids.sample(n = 71691, random_state = 42))

    with open(pathlib.Path(__file__).parent / "tweet_ids_random.txt", "w") as f:
        for val in tweet_ids_random:
            f.write('{}'.format(val))
            f.write("\n")
    
    #execute shell script at this point

def clean_tweets():
   
    filename = pathlib.Path(__file__).parent / "hydrated_tweets.json"
    
    df = pd.read_json(filename, lines = True)
    
    tweet_ids_text = []
    counter = 0
    for ele in df["data"]:
        for val in ele:
            tweet_ids_text.append((val['id'], val['text']))
            counter += 1

    with open(pathlib.Path(__file__).parent / "tweets_text_content.csv", "w") as f:
        for val in tweet_ids_text:
            f.write('{}'.format(val))
            f.write("\n")

    
     

 