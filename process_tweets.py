#!/usr/bin/python

#########################################################
# DES: Process tweets to remove punctuation.
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Ensure in correct directory:
########################################################
import os

current_dir = os.getcwd()
print("Current directory: ", current_dir)

if current_dir[len(current_dir)-3:len(current_dir)] != 'SSP':
    try:
        os.chdir(r"..\\")
        print("Changing working directory to: ", os.getcwd())
        print("New working directory: ", os.getcwd())
    except:
        print(r"Can't find ..\ folder, will try '../' instead (Windows v UNIX) ")
    try:
        os.chdir(r"../")
        print("Changing working directory to: ", os.getcwd())
        print("New working directory: ", os.getcwd())
    except:
        print(r"Still can't find correct directory, continuing script anyway")
else:
    print("Working directory already correct: ", os.getcwd())

#########################################################
# Libraries and source scripts:
#########################################################

# Libraries:
import pandas as pd
import re
import missingno as msno
import random



#########################################################
# Get data:
#########################################################

# Read in Media tweets:
media_tweets = pd.read_csv("./get_tweets/combined_tweets.csv")

##########################################################################
# Transform:
##########################################################################

# Check for duplicates:
media_tweets.drop_duplicates()

# Check for NA values:
msno.matrix(media_tweets, figsize= (50,30))
# NA columns not important.

#  Make new column for processed name nad hashtags where possible:
media_tweets['PROCESSED_TEXT'] = media_tweets['FULL_TEXT'].map(lambda i: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", '', i))
media_tweets['PROCESSED_HASHTAG'] = media_tweets['HASHTAGS'].map(lambda i: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)|(text)|(indices)|[0-9]+", '', i))

media_tweets = media_tweets[['TWEET_ID', 'DATE_TIME', 'TWITTER_ACC', 'STR_ID',
                               'FULL_TEXT', 'HASHTAGS', 'SOURCE', 'FAV_COUNT', 'RT_COUNT', 'FOLLOWERS',
                               'TWEET_COUNT', 'REPLY_TO_USER_ID', 'REPLY_TO_USER', 'LEN_TWEET',
                               'PROCESSED_TEXT', 'PROCESSED_HASHTAG']]

# Write out test dataset for testing locally.
'''
sample_list = []
for i in range (0, 2000):
    sample_list.append(random.randint(1, len(media_tweets)-1))
sample_list = sorted(sample_list)

sample_df = pd.DataFrame()
for i in sample_list:
    new_data = media_tweets[]
    pd.concat(sample_df)
'''

media_tweets[300000:302000].to_csv("./processed_tweets_sample.csv", index= False, header=None)

# Write out full dataset for running sentiment analysis in HDFS.
media_tweets.to_csv("./processed_tweets.csv", index= False, header=None)

##########################################################################

# Now that input data is cleaned for sentiment analysis in HDFS, send all files to cloud in Script 3: send_files_to_cloud.py
