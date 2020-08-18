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
import warnings
#warnings.filterwarnings("ignore")

#########################################################
# Mapper:
#########################################################

# (tweet_id 0, date 1, source 2, str_id 3, login_device 4, fav_count 5, rt_count 6, followers 7,
# tweet_count 8, reply_ind 9, reply_user_id 10, len_tweet 11, processed_text 12, processed_hashtag 13,
# filtered_processed_text 14, covid_total_count 15)

for line in csv.reader(sys.stdin): # line = row of data points, uses csv reader to split data.
    if len(line) == 16:
        date = line[1]
        source = str(line[2])
        login_device = str(line[4])
        fav_count = int(line[5])
        rt_count = int(line[6])
        followers = int(line[7])
        processed_txt = str(line[14])
        covid_count = int(line[15])
        blob = TextBlob(processed_txt)
        sentiment = float(blob.sentiment.polarity)
        if sentiment >= 0:
            sentiment_rnd = int(1)
        else:
            sentiment_rnd = int(-1)

        print(('%s,%s,%s,%s,%s,%s,%s,%s,%s') %
              (date, "MEDIA_TWITTER_ACC", fav_count, rt_count, followers, login_device, sentiment, sentiment_rnd, covid_count))
    else:
        continue
