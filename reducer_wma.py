#!/usr/bin/python3

#########################################################
# DES: Reducer for Weighted Moving average of sentiment timeseries.
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

hours = [3,5,10]

print("DATE_TIME,MEAN_SENT_CATG,WMA_3,WMA_5,WMA_10,WMA_3_ERROR,WMA_5_ERROR,WMA_10_ERROR")

# Reduce by date:
for key_value in csv.reader(sys.stdin):
    if key_value[0] != "DATE_TIME": # ensure skips line 1

        this_date_key = key_value[0]
        sent = float(key_value[2])
        sent_list3.append(sent)
        sent_list5.append(sent)
        sent_list10.append(sent)

        # WMA 3 days
        if len(sent_list3) == hours[0]+1: # for SMA3, collect 4 values, and average 1,2,3. Prediction  = 4th value
            weighted_ts3 = (sent_list3[2]*(0.5*3))+(sent_list3[1]*(0.3*3))+(sent_list3[0]*(0.2*3))
            wma_3 = weighted_ts3/hours[0] # predicted value
            wma_3_error = abs(sent-wma_3)
            del sent_list3[0]

        # WMA 5 days
        if len(sent_list5) == hours[1]+1:
            weighted_ts5 = (sent_list5[4]*(0.3*5))+(sent_list5[3]*(0.25*5))+(sent_list5[2]*(0.2*5))+(sent_list5[1]*(0.15*5))+(sent_list5[0]*(0.1*5))
            wma_5 = weighted_ts5/hours[1]
            wma_5_error = abs(sent-wma_5)
            del sent_list5[0]

        # WMA 10 days
        if len(sent_list10) == hours[2]+1:
            weighted_ts101 = (sent_list10[9]*(0.15*10))+(sent_list10[8]*(0.15*10))+(sent_list10[7]*(0.125*10))+(sent_list10[6]*(0.125*10))+(sent_list10[5]*(0.1*10))
            weighted_ts102 = (sent_list10[4]*(0.1*10))+(sent_list10[3]*(0.075*10))+(sent_list10[2]*(0.075*10))+(sent_list10[1]*(0.05*10))+(sent_list10[0]*(0.05*10))
            weighted_ts10 = weighted_ts101+weighted_ts102
            wma_10 = weighted_ts10/hours[2]
            wma_10_error = abs(sent-wma_10)
            del sent_list10[0]

        try:
            print(("%s,%s,%s,%s,%s,%s,%s,%s") % (this_date_key, sent, wma_3, wma_5, wma_10, wma_3_error, wma_5_error, wma_10_error))
        except:
            print(("%s,%s,%s,%s,%s,%s,%s,%s") % (this_date_key, sent, None, None, None, None, None, None)) # skip predictions until all values avai$


