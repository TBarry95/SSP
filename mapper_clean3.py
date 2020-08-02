#!/usr/bin/python

#########################################################
# DES: Mapper script to remove all punctuation from each tweet
#      and hashtag. Also removes domain specific jargon such as RT.
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

for line in csv.reader(sys.stdin): # line = row of data points
    if len(line) >= 13:
        tweet_id = line[0] # key = tweet_id
        date_time = line[1]
        source = line[2]
        str_id = line[3]
        full_text = line[4].lower()
        hashtags = line[5].lower()
        login_device = line[6]
        fav_count = line[7]
        rt_count = line[8]
        followers = line[9]
        tweet_count = line[10]
        reply_ind = line[11]
        reply_user_id = line[12]
        len_tweet = line[13]
        processed_text = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", '', full_text)
        processed_hashtag = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)|(text)|(indices)|[0-9]+", '', hashtags)
        print(('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s') %
              (date_time, tweet_id, source, str_id,
               fav_count, rt_count, followers, tweet_count, reply_ind,
               reply_user_id, len_tweet, processed_text, processed_hashtag))
    else:
        continue