######################################################
# DES:
# BY:
######################################################

import os
from twitter_python.accessing_published_tweets import TwitterStreamer
from twitter_python.accessing_published_tweets import TwitterAuthenticator
from twitter_python.accessing_published_tweets import TwitterClient
from twitter_python.accessing_published_tweets import TwitterListener

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

######################################################
#
######################################################

tweets = TwitterStreamer().stream_tweets("/home/tiernan/PycharmProjects/SSP/tweets.txt", ["covid19", "covid", "covid-19",
                                                                                          "coronavirus"])

#irish_tweets = TwitterClient().get_location_tweets("Ireland", 1000)

test = TwitterClient().get_hashtag_tweets(1000, "covid19")

