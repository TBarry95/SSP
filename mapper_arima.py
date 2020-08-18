#!/usr/bin/python3

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
import pandas as pd

#########################################################
# Mapper:
#########################################################

df_ts = pd.DataFrame()
sentiment_pol = []
sentiment_catg = []
data_time = []
tweet_cnt = []
covid_cnt = []

for line in csv.reader(sys.stdin):
    if len(line) == 14 and line[0] != "DATE_TIME":
        sentiment_pol.append(float(line[2]))
        sentiment_catg.append(float(line[3]))
        data_time.append(line[0])
        tweet_cnt.append(int(line[12]))
        covid_cnt.append(int(line[13]))

df_ts['DATA_TIME'] = data_time
df_ts['SENTIMENT_POLARITY'] = sentiment_pol
df_ts['SENTIMENT_CATG'] = sentiment_catg
df_ts['TWEET_COUNT'] = tweet_cnt
df_ts['COVID_COUNT'] = covid_cnt

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_ts)


