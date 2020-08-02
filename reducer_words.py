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
count_per_time = 0
favs_per_time = 0
rt_per_time  = 0
favs_to_follower = []
rt_to_follower = []

favs_to_follower.append(0)
rt_to_follower.append(0)

count_covid = 0

# (date_time, tweet_id, source, str_id,
# fav_count, rt_count, followers, tweet_count, reply_ind,
# reply_user_id, len_tweet, processed_text, processed_hashtag)

# Print column headings for output in CSV format:
print("DATE_TIME, FAVS_COUNT, RT_COUNT, TWEET_COUNT")

# Reduce by date and hour of day:
for key_value in csv.reader(sys.stdin):
    this_time_key = key_value[0]
    source = key_value[2]
    fav = int(key_value[4])
    rt = int(key_value[5])
    follower = int(key_value[6])
    text = key_value[11]

    if last_time_key == this_time_key:
        count_per_time += 1
        favs_per_time += fav  # add favs per date
        rt_per_time  += rt

    else:
        if last_time_key:
            print(('%s,%s,%s,%s') %
                  (last_time_key,
                   favs_per_time / count_per_time,
                   rt_per_time / count_per_time,  # rt:number tweets
                   count_per_time
                   ))

        # Start the reducer / restart values for each iteration
        last_time_key = this_time_key
        favs_per_time = fav
        rt_per_time = rt
        count_per_time = 1
        favs_to_follower = []
        rt_to_follower = []
        favs_to_follower.append(0)
        rt_to_follower.append(0)

        # Add actual data:
        favs_to_follower.append(fav / follower)
        rt_to_follower.append(rt / follower)


# Output summary stats:
if last_time_key == this_time_key:
    print(('%s,%s,%s,%s') %
          (last_time_key,
           favs_per_time / count_per_time,
           rt_per_time / count_per_time,  # rt:number tweets
           count_per_time
           ))