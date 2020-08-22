#!/usr/bin/python3

#########################################################
# DES: Reducer for Simple Moving average of sentiment timeseries.
#      SMA model will predict next day using 3,5 and 10 day moving average.
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

print("DATE_TIME,MEAN_SENT_CATG,SMA_3,SMA_5,SMA_10,SMA_3_ERROR,SMA_5_ERROR,SMA_10_ERROR")

# Reduce by date:
for key_value in csv.reader(sys.stdin):
    if key_value[0] != "DATE_TIME": # ensure skips line 1

        this_date_key = key_value[0]
        sent = float(key_value[2])
        sent_list3.append(sent)
        sent_list5.append(sent)
        sent_list10.append(sent)

        # SMA 3 days
        if len(sent_list3) == days[0]+1: # for SMA3, collect 4 values, and average 1,2,3. Prediction  = 4th value
            sma_3 = sum(sent_list3[0:3])/days[0] # predicted value
            sma_3_error = abs(sent-sma_3)
            #sma_3_error = ((sent-sma_3)/sent)*100
            del sent_list3[0]

        # SMA 5 days
        if len(sent_list5) == days[1]+1:
            sma_5 = sum(sent_list5[0:5])/days[1]
            sma_5_error = abs(sent-sma_5)
            #sma_5_error = ((sent-sma_5)/sent)*100
            del sent_list5[0]

        # SMA 10 days
        if len(sent_list10) == days[2]+1:
            sma_10 = sum(sent_list10[0:10])/days[2]
            sma_10_error = abs(sent-sma_10)
            #sma_10_error = ((sent-sma_10)/sent)*100
            del sent_list10[0]

        # Get error terms in %:
        #sma_3_error = ((sent-sma_3)/sent)*100
        #sma_5_error = ((sent-sma_5)/sent)*100
        #sma_10_error = ((sent-sma_10)/sent)*100

        try:
            print(("%s,%s,%s,%s,%s,%s,%s,%s") % (this_date_key, sent, sma_3, sma_5, sma_10, sma_3_error, sma_5_error, sma_10_error))
        except:
            print(("%s,%s,%s,%s,%s,%s,%s,%s") % (this_date_key, sent, None, None, None, None, None, None)) # skip predictions until all values availble (day 10)
