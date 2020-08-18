#!/usr/bin/python3

#########################################################
# DES: Mapper script used once punctuation is remove from text.
#      This mapper removes all stop words and reduces text data into essential words.
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries and source scripts:
#########################################################

import pandas as pd
import csv
import sys
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_sm")
#import warnings
#warnings.filterwarnings("ignore")

#########################################################
# Mapper:
#########################################################

for line in csv.reader(sys.stdin):
    if len(line) == 14:
        tweet_id = line[0]
        date = line[1]
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
        # spacy:
        processed_text_nlp = nlp(processed_text)
        filtered_processed_text = [str(i) for i in processed_text_nlp if i.is_stop == False]
        filtered_processed_text = ' '.join([i for i in filtered_processed_text])
        # covid count:
        covid_count_text = filtered_processed_text.count("covid")
        corona_count_text = filtered_processed_text.count("coronavirus")
        covid_count_ht = filtered_processed_text.count("covid")
        corona_count_ht = filtered_processed_text.count("coronavirus")
        covid_total_count = covid_count_text + corona_count_text + covid_count_ht + corona_count_ht
        print(('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s') %
              (tweet_id, date, source, str_id, login_device,
               fav_count, rt_count, followers, tweet_count, reply_ind,
               reply_user_id, len_tweet, processed_text, processed_hashtag,
		        filtered_processed_text, covid_total_count))
    else:
        continue
