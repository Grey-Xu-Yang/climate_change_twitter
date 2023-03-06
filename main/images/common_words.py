#source https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0

#Code provided by Jonathan Juarez

import numpy as np
import re

stopwords = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with", "n", "s", "i", "about", "are", "t"]

def clean_tweet(tweet):
    """
    Cleans twitter tweet given a collection of characters that are not needed
    for analysis.
    Input (tweet): a string of text
    Output (temp): new cleaned string
    """
    if type(tweet) == float:
        return ""
    temp = tweet.lower()
    temp = re.sub("'", "", temp) # to avoid removing contractions in english
    temp = re.sub("@[A-Za-z0-9_]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    temp = re.sub(r'http\S+', '', temp)
    temp = re.sub('[()!?]', ' ', temp)
    temp = re.sub('\[.*?\]',' ', temp)
    temp = re.sub("[^a-z0-9]"," ", temp)
    temp = temp.split()
    temp = [w for w in temp if not w in stopwords]
    temp = " ".join(word for word in temp)
    return temp


#Code that can be used to count the most frequent common words (not necessary for our needs currently)

# import pandas as pd

# df_tweets = pd.read_csv('../sources/tweets_text_content - tweets_text_content.csv')
# tweets_list = df_tweets.iloc[:, [1]].values

# #convert list of lists of tweets into one list
# tweets = list(np.concatenate(tweets_list))

# #clean tweets
# cleaned_tweets = [clean_tweet(tw) for tw in tweets]

# #Finding most common words in a list of strings

# from collections import Counter

# #Join element strings of tweets list into one long string
# words = " ".join(cleaned_tweets)

# print(type(words))

# # split the string into individual words
# words = words.split()

# # count the frequency of each word
# word_counts = Counter(words)

# # find the 5 most common words
# most_common_words = word_counts.most_common(10)

# print(most_common_words)
