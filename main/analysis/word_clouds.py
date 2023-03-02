import plotly.graph_objs as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
from common_words import clean_tweet


df_tweets = pd.read_csv('../sources/tweets_text_content - tweets_text_content.csv')
tweets_list = df_tweets.iloc[:, [1]].to_numpy()

tweets = list(np.concatenate(tweets_list))

#clean tweets
cleaned_tweets = [clean_tweet(tw) for tw in tweets]
#print(cleaned_tweets)

#Join element strings of tweets list into one long string
text = " ".join(cleaned_tweets)

wordcloud = WordCloud(width=800, height=400, max_words=50, background_color='white').generate(text)

fig = make_subplots(rows=1, cols=1)

#print(wordcloud.words_.values())
# print(wordcloud.words_.update((x, y + 1) for x, y in wordcloud.words_.items()))

#adding to the values of this dictionary for scatter
for key in wordcloud.words_:
    wordcloud.words_[key] += 20
words_size_values = wordcloud.words_.values()

#fig.add_trace(go.Scatter(x=[0], y=[0], mode='text', text=wordcloud.words_, textfont=dict(size=20, color='#000000')), row=1, col=1)
fig.add_trace(go.Scatter(x=[0], y=[0], mode='text', text=list(wordcloud.words_.keys()), textfont=dict(size=list(words_size_values), color='#000000')), row=1, col=1)

fig.update_layout(
    title="Most Common Words Relating to Climate Change",
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
)

fig.show()

# # Start with loading all necessary libraries
# import numpy as np
# import pandas as pd
# from os import path
# from PIL import Image
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import matplotlib.pyplot as plt
# from common_words import clean_tweet

# df_tweets = pd.read_csv('../sources/tweets_text_content - tweets_text_content.csv')
# tweets_list = df_tweets.iloc[:, [1]].values

# tweets = list(np.concatenate(tweets_list))

# #clean tweets
# cleaned_tweets = [clean_tweet(tw) for tw in tweets]


# #Join element strings of tweets list into one long string
# text = " ".join(cleaned_tweets)
# #print(text)
# #print(words)

# # Create and generate a word cloud image:
# wordcloud = WordCloud(width=800, height=400, max_words=20, background_color='white').generate(text)

# # # Display the generated image:
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("on")
# plt.show()