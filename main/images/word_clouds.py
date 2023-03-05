# Start with loading all necessary libraries
import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from common_words import clean_tweet

df_tweets = pd.read_csv('../sources/tweets_text_content - tweets_text_content.csv')
tweets_list = df_tweets.iloc[:, [1]].values
print(type(tweets_list))
tweets = list(np.concatenate(tweets_list))

#clean tweets
cleaned_tweets = [clean_tweet(tw) for tw in tweets]
print("the cleaned tweet list", len(cleaned_tweets))

#Join element strings of tweets list into one long string
text = " ".join(cleaned_tweets)
print("joined text", len(text))

stopwords = set(STOPWORDS)
stopwords.update(["said", "u", "know", "make", "thing", "much", "want", "say", "will",
              "re", "come", "going", "doesn", 'goparkansas',
              "see", "via", "amp", "wait", 'almost'])  # add additional stop words as needed
#stopwords = set(stopwords)

# Create and generate a word cloud image:
wordcloud = WordCloud(width=600, height=400, max_words=40, background_color='white', stopwords=stopwords, collocations = False).generate(text)

#print(wordcloud.words_.items())

# # Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

#this saves the wordcloud generated into an image file
#plt.savefig('wordcloud_one.png')

#possible code for implementing with plotly

# import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# from wordcloud import WordCloud, STOPWORDS
# import pandas as pd
# import numpy as np
# from common_words import clean_tweet

# df_tweets = pd.read_csv('../sources/tweets_text_content - tweets_text_content.csv')
# tweets_list = df_tweets.iloc[:, [1]].to_numpy()

# tweets = list(np.concatenate(tweets_list))

# #clean tweets
# cleaned_tweets = [clean_tweet(tw) for tw in tweets]
# #print(cleaned_tweets)

# #Join element strings of tweets list into one long string
# text = " ".join(cleaned_tweets)

# stopwords = list(STOPWORDS)
# stopwords += ["said", "u", "know", "make", "thing", "much", "want", "say", "will",
#               "re", "come", "going", "change doesn'", "doesn see"]  # add additional stop words as needed

# wordcloud = WordCloud(width=800, height=400, max_words=50, background_color='white', stopwords=stopwords).generate(text)

# fig = make_subplots(rows=1, cols=1)


# #adding to the values of this dictionary for scatter
# for key in wordcloud.words_:
#     wordcloud.words_[key] += 50
# words_size_values = wordcloud.words_.values()

# #print(type(list(wordcloud.words_.keys())))

# #fig.add_trace(go.Scatter(x=[0], y=[0], mode='text', text=wordcloud.words_, textfont=dict(size=20, color='#000000')), row=1, col=1)
# #fig.add_trace(go.Scatter(x=[0], y=[0], mode='text', text=list(wordcloud.words_.keys()), textfont=dict(size=list(words_size_values), color='#000000')), row=1, col=1)

# for i, (word, count) in enumerate(wordcloud.words_.items()):
#     fig.add_trace(
#         go.Scatter(
#             x=[i % 10],
#             y=[-(i // 10)],
#             mode="text",
#             text=[word],
#             textfont=dict(size=count, color='#000000')
#         )
#     )

# fig.update_layout(
#     title="Common Words in Climate Change Twitter Data",
#     xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
#     yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
# )

# fig.show()
