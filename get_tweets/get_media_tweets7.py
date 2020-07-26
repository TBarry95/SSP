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

twitter_pgs7 = ["NBCNewsHealth", "healthmagazine", "MensHealthMag", "WomensHealthMag",
                "Twitter", "cheddar", "SportsCenter", "NFL", "LovinDublin", "JOEdotie",
                "Herdotie", "rollingstone", "natgeosociety", "foxnews", "engadget",
                "arstechnica", "EFF", "verge", "ZDNet", "ACLU", "SenateDems"]

tweets_list7 = fns1.get_tweets_list(twitter_pgs7, 130)

tweets_df7 = fns1.tweets_to_df1(tweets_list7)

tweets_df7.to_csv("./media_tweets7.csv", index= False)
