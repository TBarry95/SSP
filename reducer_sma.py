#!/usr/bin/python3

#########################################################
# DES: Reducer for Moving average of sentiment timeseries.
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries and source scripts:
#########################################################

import sys
import csv

#########################################################
# reducer:
#########################################################

sent_list3 = []
sent_list5 = []
sent_list10 = []

days = [3,5,10]

# Reduce by date:
for key_value in csv.reader(sys.stdin):
    if key_value[0] != "DATE_TIME": # ensure skips line 1

        this_date_key = key_value[0]
        sent = float(key_value[2])
        sent_list3.append(sent)
        sent_list5.append(sent)
        sent_list10.append(sent)

        if len(sent_list3) == days[0]:
            sum_sent3 = 0
            for i in sent_list3:
                sum_sent3 += i
            sma_3 = sum_sent3/days[0]
            del sent_list3[0]

        if len(sent_list5) == days[1]:
            sum_sent5  = 0
            for i in sent_list5:
                sum_sent5 += i
            sma_5 = sum_sent5/days[1]
            del sent_list5[0]

        if len(sent_list10) == days[2]:
            sum_sent10 = 0
            for i in sent_list10:
                sum_sent10 += i
            sma_10 = sum_sent10/days[2]
            del sent_list10[0]

        try:
            print(("%s,%s,%s,%s,%s") % (this_date_key, sent, sma_3, sma_5, sma_10))
        except:
            print(("%s,%s,%s,%s,%s") % (this_date_key, sent, None, None, None))
