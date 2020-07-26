#!/usr/bin/python

#########################################################
# DES: Get media tweets from specified twitter pages
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Ensure in correct directory:
########################################################
import os

current_dir = os.getcwd()
print("Current directory: ", current_dir)

if current_dir[len(current_dir)-10:len(current_dir)] != 'get_tweets':
    try:
        os.chdir(r".\get_tweets")
        print("Changing working directory to: ", os.getcwd())
        print("New working directory: ", os.getcwd())
    except:
        print(r"Can't find .\get_tweets folder, will try '/get_tweets' instead (Windows v UNIX) ")
    try:
        os.chdir(r"./get_tweets")
        print("Changing working directory to: ", os.getcwd())
        print("New working directory: ", os.getcwd())
    except:
        print(r"Still can't find correct directory, continuing script anyway")
else:
    print("Working directory already correct: ", os.getcwd())

#########################################################
# Libraries and source scripts:
#########################################################

import functions_twitter as fns1
import pandas as pd

#########################################################
# Get data:
#########################################################

twitter_pgs7 = ["NBCNewsHealth", "healthmagazine", "MensHealthMag", "WomensHealthMag",
                "Twitter", "cheddar", "SportsCenter", "NFL", "LovinDublin", "JOEdotie",
                "Herdotie", "rollingstone", "natgeosociety", "foxnews", "engadget",
                "arstechnica", "EFF", "verge", "ZDNet", "ACLU", "SenateDems"]

# Remove comments to refresh tweets:
#tweets_list7 = fns1.get_tweets_list(twitter_pgs7, 130)
#tweets_df7 = fns1.tweets_to_df1(tweets_list7)
#tweets_df7.to_csv("./media_tweets7.csv", index= False)
