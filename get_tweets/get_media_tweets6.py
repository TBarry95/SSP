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

twitter_pgs6 = ["ScienceNews", "newscientist", "DiscoverMag", "sciam", "PopSci", "ScienceMagazine",
                "CNET", "ladbible", "WorldAndScience", "BBCScienceNews", "guardianscience", "WIREDScience",
                "NYTScience", "NYTHealth", "NPRHealth", "HarvardHealth", "MayoClinic", "AmerMedicalAssn",
                "ClevelandClinic", "NIH"]

tweets_list6 = fns1.get_tweets_list(twitter_pgs6, 130)

tweets_df6 = fns1.tweets_to_df1(tweets_list6)

tweets_df6.to_csv("./media_tweets6.csv", index= False)
