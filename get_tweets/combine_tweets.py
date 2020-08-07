#!/usr/bin/python

#########################################################
# DES: Combine all tweets into 1 dataframe and export.
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

import pandas as pd

#########################################################
# Get data:
#########################################################

media_tweets1 = pd.read_csv("./media_tweets1.csv")
media_tweets2 = pd.read_csv("./media_tweets2.csv")
media_tweets3 = pd.read_csv("./media_tweets3.csv")
media_tweets4 = pd.read_csv("./media_tweets4.csv")
media_tweets5 = pd.read_csv("./media_tweets5.csv")
media_tweets6 = pd.read_csv("./media_tweets6.csv")
media_tweets7 = pd.read_csv("./media_tweets7.csv")
media_tweets8 = pd.read_csv("./media_tweets8.csv")
media_tweets9 = pd.read_csv("./media_tweets9.csv")

#########################################################
# Combine all files into 1:
#########################################################

all_tweets = pd.concat([media_tweets1, media_tweets2, media_tweets3, media_tweets4, media_tweets5,
                        media_tweets6, media_tweets7, media_tweets8, media_tweets9])

#########################################################
# Export:
#########################################################

all_tweets.to_csv("./combined_tweets.csv", index= False)
all_tweets.to_csv("./combined_tweets_noheader.csv", index= False, header=False)