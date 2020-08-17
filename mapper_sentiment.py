#!/usr/bin/python3

#########################################################
# DES: Mapper script applies a sentiment score for each tweet.
#      Using the date as the key, mapper returns:
#      the date, source, fav_count, rt_count, followers, login_device, sentiment from each tweet.
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries and source scripts:
#########################################################

import sys
from textblob import TextBlob
import csv
#import warnings
#warnings.filterwarnings("ignore")

#########################################################
# Mapper:
#########################################################

# (tweet_id 0, date 1, source 2, str_id 3, login_device 4, fav_count 5, rt_count 6, followers 7,
# tweet_count 8, reply_ind 9, reply_user_id 10, len_tweet 11, processed_text 12, processed_hashtag 13,
# filtered_processed_text 14)

for line in csv.reader(sys.stdin): # line = row of data points, uses csv reader to split data.
    if len(line) >= 13:
        date = line[1]
        source = line[2]
        login_device = line[4]
        fav_count = line[5]
        rt_count = line[6]
        followers = line[7]
        processed_txt = line[14]
        blob = TextBlob(processed_txt)
        sentiment = blob.sentiment.polarity
        if sentiment >= 0:
            sentiment_rnd = 1
        else:
            sentiment_rnd = -1

        print(('%s,%s,%s,%s,%s,%s,%s,%s') %
              (date, "MEDIA_TWITTER_ACC", fav_count, rt_count, followers, login_device, sentiment, sentiment_rnd))
        #print(('%s,%s,%s,%s,%s,%s,%s,%s') % (0, date, "MEDIA", fav_count, rt_count, followers, login_device, sentiment))
        #print(('%s,%s,%s,%s,%s,%s,%s,%s') % (1, date, source, fav_count, rt_count, followers, login_device, sentiment))
    else:
        continue
