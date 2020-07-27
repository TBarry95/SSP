#!/usr/bin/python3

#########################################################
# DES: Mapper script used once punctuation is remove from text.
#      This mapper removes all stop words and reduces text data into essential words.
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries and source scripts:
#########################################################

#from nltk.corpus import stopwords
#import nltk
#from nltk.tokenize import word_tokenize
import csv
import sys
import re
#nltk.download('stopwords')
#nltk.download('punkt')
#import warnings
#warnings.filterwarnings("ignore")

#########################################################
# Mapper:
#########################################################

for line in csv.reader(sys.stdin): # line = row of data points
    if len(line) >= 13:
        tweet_id = line[0] # key = tweet_id
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

        #stopwords_list = stopwords.words('english')
        #processed_txt_token = word_tokenize(processed_txt)
        #filtered_processed_text = [i for i in processed_txt_token if i not in stopwords_list]
        #filtered_processed_text = ' '.join(filtered_processed_text)

        print(('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s') %
              (tweet_id, date, source, str_id, login_device,
               fav_count, rt_count, followers, tweet_count, reply_ind,
               reply_user_id, len_tweet, processed_text, processed_hashtag))
    else:
        continue