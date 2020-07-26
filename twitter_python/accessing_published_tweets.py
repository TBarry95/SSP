######################################################
# DES: Python module for interacting with twitter API. This file was originally sourced from
#      the following git repository:
#      https://github.com/vprusso/youtube_tutorials/tree/master/twitter_python/part_2_cursor_and_pagination
#      Vairous updates have been made based on project requirements.
# BY:  Tiernan BArry
######################################################

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#import twitter_credentials

from . import twitter_credentials

######################################################
# TWITTER CLIENT
######################################################

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_timeline_pages(self, num_of_pages):
        page_list = []
        for i in Cursor(self.twitter_client.user_timeline, id=self.twitter_user, tweet_mode='extended',
                        wait_on_rate_limit=True).pages(num_of_pages):
            page_list.append(i)
        return page_list

    def get_hashtag_tweets(self, num_of_tweets, hashtag):
        tweet_list = []
        for i in Cursor(self.twitter_client.search, q=hashtag, lang="en", tweet_mode='extended', wait_on_rate_limit=True).pages(num_of_tweets):
            tweet_list.append(i)
            return tweet_list

    def get_location_tweets(self, country, num_of_tweets):
        tweet_list = []
        places = self.twitter_client.geo_search(query=country, granularity="country")
        place_id = places[0].id
        tweets = Cursor(self.twitter_client.search, q="place:%s" % place_id, tweet_mode='extended',
                        wait_on_rate_limit=True).items(num_of_tweets)
        for i in tweets:
            tweet_list.append(i)
            # print(i.text + " | " + i.place.name if i.place else "Undefined place")
        return tweet_list


######################################################
# TWITTER AUTHENTICATER
######################################################

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

######################################################
# TWITTER STREAMER
######################################################

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)
        stream.filter()

######################################################
# TWITTER STREAM LISTENER
######################################################

class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)
