import pathlib
import pandas as pd
#extracting random tweet ids - Ridhi Purohit

def extract_tweet_ids():
    '''
    This function extracts tweet ids from the larger data set for tweets which were located in the US.
    Post extracting the tweet ids, a txt file is created to store them which is then fed into a shell script
    to extract hydrated tweets using "twarc".

    Output: Creates a "tweet_ids_random.txt" file with randomized tweet ids extracted from the 
    US_twitter_analysis_county.csv
    '''
    filename1 = pathlib.Path(__file__).parent.parent / "sources" / "merged_date_county.csv"

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


def clean_tweets():
    '''
    This function extracts tweet ids and tweet text from the twarc output file "hydrated_tweets.json".
    This json file contains data for 60,323 which is around 10,000 less than the what was meant to be distracted. 
    The missing tweets are the archived tweets per "twarc.log" file.

    Output: Creates a "tweet_text_content.csv" file with a tuples containing tweet ids and tweet text extracted from the 
    hydrated_tweets.json
    '''
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

def call_extraction():
    '''
    This function calls a function to extract tweet ids. After this step is executed, tweets_extraction.sh is
    executed to hydrate the tweet ids.
    '''
    extract_tweet_ids()

def perform_clean():
    '''
    This function is executed after tweets_extraction.sh to extract tweet ids and text content from 
    "hydrated_tweets.json" file by calling the relevant function.
    '''

    extract_tweet_ids()


    
     

 
