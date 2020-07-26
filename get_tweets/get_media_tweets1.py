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
import os

#########################################################
# Ensure in correct directory:
########################################################

os.chdir()

#########################################################
# Get data:
#########################################################

twitter_pgs1 = ["CNN", "BBCWorld", "BBCBreaking", "BBCNews", "ABC", "Independent",
               "RTENewsNow", "Independent_ie", "guardian", "guardiannews", "rtenews", "thejournal_ie",
               "wef", "IMFNews", "WHO", "euronews", "MailOnline", "TheSun", "Daily_Express", "DailyMirror"]

tweets_list1 = fns1.get_tweets_list(twitter_pgs1, 130)

tweets_df1 = fns1.tweets_to_df1(tweets_list1)

tweets_df1.to_csv("./media_tweets1.csv", index= False)
