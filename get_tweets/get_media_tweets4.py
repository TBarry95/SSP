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

twitter_pgs4 = ["mashable", "TechCrunch", "big_picture", "TheOnion", "espn", "harvardbiz", "gizmodo", "whitehouse",
                "wired",  "smashingmag", "pitchforkmedia", "peoplemag", "newsweek", "huffingtonpost", "bbcclick",
                "eonline", "rww", "instyle", "mtv", "freakonomics"]

tweets_list4 = fns1.get_tweets_list(twitter_pgs4, 130)

tweets_df4 = fns1.tweets_to_df1(tweets_list4)

tweets_df4.to_csv("./media_tweets4.csv", index= False)
