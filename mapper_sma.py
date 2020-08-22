#!/usr/bin/python3

#########################################################
# DES: Moving averages mapper
#      Number of days: 
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

for line in csv.reader(sys.stdin):
    if len(line) == 14: #and str(line[0]) != str("DATE_TIME"):
        date = line[0]
        sent_pol = line[2]
        sent_catg = line[3]
        covd_count = line[13]
    print(('%s,%s,%s,%s') % (date, sent_pol, sent_catg, covd_count))


