#source https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0
import numpy as np
import re

stopwords = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

def clean_tweet(tweet):
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

tweets = ["Get ready for #NatGeoEarthDay! Join us on 4/21 for an evening of music and celebration, exploration and inspiration https://on.natgeo.com/3t0wzQy.",
"Coral in the shallows of Aitutaki Lagoon, Cook Islands, Polynesia https://on.natgeo.com/3gkgq4Z",
"Don't miss our @reddit AMA with author and climber Mark Synnott who will be answering your questions about his historic journey to the North Face of Everest TODAY at 12:00pm ET! Start submitting your questions here: https://on.natgeo.com/3ddSkHk @DuttonBooks"]

cleaned_tweets = [clean_tweet(tw) for tw in tweets]
print(results)

#Finding most common words in a list of strings

from collections import Counter

#Join element strings of tweets list into one long string
words = " ".join(cleaned_tweets)
#print(words)

# split the string into individual words
words = words.split()

# count the frequency of each word
word_counts = Counter(words)

# find the 5 most common words
most_common_words = word_counts.most_common(5)

print(most_common_words)
