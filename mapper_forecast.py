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

df_timeseries =

for line in csv.reader(sys.stdin): # line = row of data points
    if len(line) >= 4:
        date_time = line[0]
        tweet_id = line[1]
        source = line[2]
        str_id = line[3]
        fav_count = line[4]

