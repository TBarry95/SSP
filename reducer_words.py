#!/usr/bin/python

#########################################################
# DES:
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

last_time_key = None
favs_per_time = 0
rt_per_time  = 0
count_per_time = 0
aggregate_covid_count = 0

# favs_to_follower = []
# rt_to_follower = []
# favs_to_follower.append(0)
# rt_to_follower.append(0)

# (date_time, tweet_id, source, str_id,
# fav_count, rt_count, followers, tweet_count, reply_ind,
# reply_user_id, len_tweet, processed_text, processed_hashtag,
#  total_count)

# Print column headings for output in CSV format:
print("DATE_TIME, FAVS_COUNT, RT_COUNT, TWEET_COUNT, COVID_COUNT")

# Reduce by date and hour of day:
for key_value in csv.reader(sys.stdin):
    try:
        this_time_key = key_value[0]
        tweet_id = key_value[1]
        source = key_value[2]
        fav = int(key_value[4])
        rt = int(key_value[5])
        follower = int(key_value[6])
        tweet_count = int(key_value[7])
        reply_ind = key_value[8]
        reply_user_id = key_value[9]
        len_tweet = int(key_value[10])
        text = key_value[11]
        processed_hashtag = key_value[12]
        covid_count = int(key_value[13])

        if last_time_key == this_time_key:
            favs_per_time += int(fav)  # add favs per date
            rt_per_time  += int(rt)
            count_per_time += 1
            aggregate_covid_count += covid_count

        else:
            if last_time_key:
                print(('%s,%s,%s,%s,%s') %
                      (last_time_key,
                       favs_per_time,
                       rt_per_time,
                       count_per_time,
                       aggregate_covid_count
                       ))

            # Start the reducer / restart values for each iteration
            last_time_key = this_time_key
            favs_per_time = fav
            rt_per_time = rt
            count_per_time = 1
            aggregate_covid_count = covid_count

    except:
        continue

# Output summary stats:
if last_time_key == this_time_key:
    print(('%s,%s,%s,%s,%s') %
        (last_time_key,
        favs_per_time,
        rt_per_time,
        count_per_time,
        aggregate_covid_count
        ))