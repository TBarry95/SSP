#!/usr/bin/python

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
warnings.filterwarnings("ignore")

#########################################################
# Mapper:
#########################################################

# (tweet_id, date, source, login_device, fav_count, rt_count, followers, filtered_processed_text))

for line in csv.reader(sys.stdin): # line = row of data points, uses csv reader to split data.
    if len(line) >= 7:
        date = line[1]
        source = line[2]
        login_device = line[3]
        fav_count = line[4]
        rt_count = line[5]
        followers = line[6]
        processed_txt = line[7]
        blob = TextBlob(processed_txt)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            sentiment_rnd = 1
        else:
            sentiment_rnd = -1

        print(('%s,%s,%s,%s,%s,%s,%s') % (date, "MEDIA", fav_count, rt_count, followers, login_device, sentiment, sentiment_rnd))
        #print(('%s,%s,%s,%s,%s,%s,%s,%s') % (0, date, "MEDIA", fav_count, rt_count, followers, login_device, sentiment))
        #print(('%s,%s,%s,%s,%s,%s,%s,%s') % (1, date, source, fav_count, rt_count, followers, login_device, sentiment))
    else:
        continue
