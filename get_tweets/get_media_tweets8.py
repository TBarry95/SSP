#!/usr/bin/python

#########################################################
# DES: Get media tweets from specified twitter pages
# BY:  Tiernan Barry, x19141840 - NCI.
#########################################################

#########################################################
# Libraries and source scripts:
#########################################################

import functions_ssp as fns1
import pandas as pd

#########################################################
# Get data:
#########################################################

twitter_pgs8 = ["GOP", "HouseGOP", "HouseDemocrats", "NASA", "NBA", "VanityFair", "AmerMedicalAssn",
                "TrendMicro", "kaspersky", "DarkReading", "offsectraining", "USCERT_gov", "FireEye",
                "CiscoSecure", "NBCNewsHealth", "SELFmagazine", "USATODAYhealth",
                "Shape_Magazine", "Allure_magazine", "POPSUGARFitness"]

tweets_list8 = fns1.get_tweets_list(twitter_pgs8, 130)

tweets_df8 = fns1.tweets_to_df1(tweets_list8)

tweets_df8.to_csv("./media_tweets8.csv", index= False)
