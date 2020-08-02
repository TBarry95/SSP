#!/usr/bin/python

#########################################################
# DES:
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries and source scripts:
#########################################################

import csv
import sys
import re

#########################################################
# Mapper:
#########################################################

# Input cols:
# (date_time, tweet_id, source, str_id,
# fav_count, rt_count, followers, tweet_count, reply_ind,
# reply_user_id, len_tweet, processed_text, processed_hashtag))

for line in csv.reader(sys.stdin): # line = row of data points
    if len(line) >= 13:
        date_time = line[0]
        tweet_id = line[1]
        source = line[2]
        str_id = line[3]
        fav_count = line[4]
        rt_count = line[5]
        followers = line[6]
        tweet_count = line[7]
        reply_ind = line[8]
        reply_user_id = line[9]
        len_tweet = line[10]
        processed_text = line[11]
        processed_hashtag = line[12]
        covid_count_text = processed_text.count("covid")
        corona_count_text = processed_text.count("coronavirus")
        covid_count_ht = processed_hashtag.count("covid")
        corona_count_ht = processed_hashtag.count("coronavirus")
        total_count = covid_count_text + corona_count_text + covid_count_ht + corona_count_ht
        print(('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s') %
              (date_time, tweet_id, source, str_id,
               fav_count, rt_count, followers, tweet_count, reply_ind,
               reply_user_id, len_tweet, processed_text, processed_hashtag,
               total_count))
    else:
        continue