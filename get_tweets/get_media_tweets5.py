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

twitter_pgs5 = ["todayshow", "good", "gawker", "msnbc_breaking", "guardiantech", "usweekly", "life",
                "cnnmoney", "nprpolitics", "nytimesphoto", "io9", "sciencechannel", "usabreakingnews", "vanityfairmag",
                "themoment", "davos", "planetmoney", "politico"]

tweets_list5 = fns1.get_tweets_list(twitter_pgs5, 130)

tweets_df5 = fns1.tweets_to_df1(tweets_list5)

tweets_df5.to_csv("./media_tweets5.csv", index= False)
