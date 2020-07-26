
import os
import tweepy as tw
import pandas as pd


access_token = "1226993301410209794-gJsrEx4oNWY7Bq7z2UD2y8P5GtSZeP"
access_token_secret = "o5el2hcy4IQq37rNl1OQxYVCiUs6vLY9xK8CLYczRUcJk"
consumer_key = "yEWIZAFmCVp2bAfhmgIhmWuQJ"
consumer_secret = "IXgkHxWVrooJdskm5rQr059nPWymEsexcNfWZ3lfO0z7IYltaB"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


# Define the search term and the date_since date as variables
search_words = "#covid"
date_since = "2018-11-16"

# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(10000)

tweets_list = []
for tweet in tweets:
    tweets_list.append(tweet.text)




