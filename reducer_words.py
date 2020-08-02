#!/usr/bin/python

#########################################################
# DES: Reducer script to find insights regarding sentiment analysis scores for each date.
#      On a follower weighted basis, as well as a tweets per day basis, finds insights
#      such as average sentiment scores per date, and correlations between sentiment scores and favourites/RTs.
#      Please note:
#      Because standard deviation require at least 2 values per date, and because there are some dates with only 1 tweet,
#      this reducer adds a 0 to all lists to fulfill these requirements. The assumption is that dates with only 2 tweets these
#      values are meaningless anyway, while others they will not impact.
#      Similarily, when only 1 tweet is couneted per date, Scipy prints out a warning when calculating correlation coefficient.
#      This is why warnings are disabled, as the return is 'nan' for such dates.
#      Results are manually copied from HDFS into the Ubuntu EC2 machine using 'hdfs dfs -copyToLocal'.
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries and source scripts:
#########################################################

import sys
import csv
import warnings


#########################################################
# Reducer:
#########################################################

last_date_key = None
count_per_date = 0
favs_per_dt = 0
rt_per_dt = 0
aggregate_sentiment = 0
aggregate_sentiment_rnd = 0 # new variable for categorical sentiment
sent_list_sort = SortedList()
list_sentiment = []
list_sentiment_rnd = []
favs_to_follower = []
rt_to_follower = []


