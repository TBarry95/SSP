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

twitter_pgs3 = ["NPR", "AP", "USATODAY", "NYDailyNews", "nypost", "BBCLondonNews", "DailyMailUK",
               "CBSNews", "MSNBC", "nytimes", "FT", "business", "cnni", "RT_com", "AJEnglish", "CBS", "NewsHour",
               "BreakingNews", "cnnbrk", "WSJ", "Reuters", "SkyNews", "CBCAlerts"]

tweets_list3 = fns1.get_tweets_list(twitter_pgs3, 120)

tweets_df3 = fns1.tweets_to_df1(tweets_list3)

tweets_df3.to_csv("./media_tweets3.csv", index= False)

