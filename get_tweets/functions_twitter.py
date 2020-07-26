#!/usr/bin/python

#########################################################
# DES: Support script for defining functions.
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries:
#########################################################

import pandas as pd
import twitter_python.accessing_published_tweets as twt

#########################################################
# Extract:
#########################################################

def get_tweets_list(list_of_twitter_accs, num_pages):
    tweet_list = []
    for i in list_of_twitter_accs:
        try:
            tweet_list.append(twt.TwitterClient(twitter_user=i).get_timeline_pages(num_pages))
            print("Tweets successfully sourced from : ", i)
        except:
            print("Error fetching Twitter data for :", i)
    all = []
    for i in tweet_list:
        for ii in i:
            for iii in ii:
                all.append(iii)
    return all

def get_irish_tweets_list(country,num_pages):
    tweet_list = []
    tweets = twt.TwitterClient().get_location_tweets(country, num_pages)
    for i in tweets:
        tweet_list.append(i)
    return tweet_list

def tweets_to_df(all):
    df_all_tweets = pd.DataFrame()
    df_all_tweets['TWEET_ID'] = [i.id for i in all]
    df_all_tweets['DATE_TIME'] = [str(i.created_at)[0:13] for i in all]
    df_all_tweets['TWITTER_ACC'] = [i.user.name for i in all]
    df_all_tweets['STR_ID'] = [i.id_str for i in all]
    df_all_tweets['FULL_TEXT'] = [i.full_text for i in all]
    df_all_tweets['HASHTAGS'] = [i.entities['hashtags'] for i in all]
    df_all_tweets['SOURCE'] = [i.source for i in all]
    df_all_tweets['FAV_COUNT'] = [i.favorite_count for i in all]
    df_all_tweets['RT_COUNT'] = [i.retweet_count for i in all]
    df_all_tweets['FOLLOWERS'] = [i.user.followers_count for i in all]
    df_all_tweets['TWEET_COUNT'] = [i.author.statuses_count for i in all]
    df_all_tweets['REPLY_TO_USER_ID'] = [i.in_reply_to_user_id for i in all]
    df_all_tweets['REPLY_TO_USER'] = [i.in_reply_to_screen_name for i in all]
    df_all_tweets['LEN_TWEET'] = [len(i) for i in df_all_tweets['FULL_TEXT']]
    df_all_tweets.sort_values(by='DATE_TIME', ascending=0)
    return df_all_tweets

def tweets_to_df1(all):
    df_all_tweets = pd.DataFrame()
    df_all_tweets['TWEET_ID'] = [i.id for i in all]
    df_all_tweets['DATE_TIME'] = [str(i.created_at)[0:13] for i in all]
    df_all_tweets['TWITTER_ACC'] = [i.user.name for i in all]
    df_all_tweets['STR_ID'] = [i.id_str for i in all]
    df_all_tweets['FULL_TEXT'] = [i.full_text for i in all]
    df_all_tweets['HASHTAGS'] = [i.entities['hashtags'] for i in all]
    df_all_tweets['SOURCE'] = [i.source for i in all]
    df_all_tweets['FAV_COUNT'] = [i.favorite_count for i in all]
    df_all_tweets['RT_COUNT'] = [i.retweet_count for i in all]
    df_all_tweets['FOLLOWERS'] = [i.user.followers_count for i in all]
    df_all_tweets['TWEET_COUNT'] = [i.author.statuses_count for i in all]
    df_all_tweets['REPLY_TO_USER_ID'] = [i.in_reply_to_user_id for i in all]
    df_all_tweets['REPLY_TO_USER'] = [i.in_reply_to_screen_name for i in all]
    df_all_tweets['LEN_TWEET'] = [len(i) for i in df_all_tweets['FULL_TEXT']]
    df_all_tweets.sort_values(by='DATE_TIME', ascending=0)
    return df_all_tweets

