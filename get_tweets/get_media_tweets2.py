#!/usr/bin/python

#########################################################
# DES: Get media tweets from specified twitter pages
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries and source scripts:
#########################################################

import functions_ssp as fns1
import pandas as pd


#########################################################
# Get data:
#########################################################

twitter_pgs2  = ["standardnews", "LBC", "itvnews", "thetimes", "IrishTimes", "ANI", "XHNews", "TIME", "OANN",
               "BreitbartNews", "Channel4News", "BuzzFeedNews", "NewstalkFM", "NBCNewsBusiness", "CNBCnow",
               "markets", "YahooFinance", "MarketWatch", "Forbes", "businessinsider", "thehill", "CNNPolitics"]

tweets_list2 = fns1.get_tweets_list(twitter_pgs2, 120)

tweets_df2 = fns1.tweets_to_df1(tweets_list2)

tweets_df2.to_csv("./media_tweets2.csv", index= False)

