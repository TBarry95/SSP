############################################
# DES: Plot sentiment analysis timeseries of tweets
# BY: Tiernan Barry
###########################################

import pandas as pd
import matplotlib.pyplot as plt

###########################################
# Get data:
###########################################

sentiment_results = pd.read_csv(r"./output/job_2/part-00000.csv")

###########################################
# Filter data by date:
###########################################

sentiment_results = sentiment_results[sentiment_results['DATE_TIME'].str.startswith("2020")]
plt_sentiment_results = sentiment_results[['DATE_TIME', ' MEAN_SENT_POLARITY', ' MEAN_SENT_CATG']]
plot = plt_sentiment_results.plot(kind='bar')
plot.figure
