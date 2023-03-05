#Start with loading all necessary libraries
import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from common_words import clean_tweet

df_tweets = pd.read_csv('../sources/merged_twitter_text_county.csv')

def word_cloud(data, stance, year):
    df = data[(data["stance"] == stance) & (df_tweets["fyDeclared"] == year)]

    tweets_list = df["content"].to_numpy()

    cleaned_tweets = [clean_tweet(tw) for tw in tweets_list]

    #Join element strings of tweets list into one long string
    text = " ".join(cleaned_tweets)

    stopwords = set(STOPWORDS)
    stopwords.update(["said", "u", "know", "make", "thing", "much", "want", "say", "will",
                "re", "come", "going", "doesn", 'goparkansas', 'don', 'nal',
                "see", "via", "amp", "wait", 'almost', 'im', 'wouldn'])  # add additional stop words as needed

    # Create and generate a word cloud image:
    wordcloud = WordCloud(width=600, height=400, max_words=40, background_color='white',\
     stopwords=stopwords, collocations = True).generate(text)

    # # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    #this saves the wordcloud generated into an image file
    plt.savefig(f'wordcloud_{stance}_{year}.png')
    plt.show()


