############################################
# DES: Read in results from job 2, and plot timeseries of sentiment values.
# BY: Tiernan Barry
###########################################

###########################################
# Libraries:
###########################################

import pandas as pd

###########################################
# Get data:
###########################################

# get TS data
ts_data = pd.read_csv(r"./output/job_2/part-00000.csv")
ts_data = ts_data[ts_data['DATE_TIME'].str.contains('2020-02|2020-03|2020-04|2020-05|2020-06|2020-07')]

# get results:
results_ma = pd.read_csv(r"./moving_avg_results.csv")


###########################################
# adjust data
###########################################

# Set datetime column:
format = '%Y-%m-%d %H'
ts_data['DATE_TIME'] = pd.to_datetime(ts_data['DATE_TIME'], format=format)
ts_data = ts_data.set_index(pd.DatetimeIndex(ts_data['DATE_TIME']))

# find lowest error across all:
results_ma['TOTAL'] = results_ma['MSE']+results_ma['RMSE']+results_ma['MAE']

###########################################
# Plot:
###########################################

# plot TS of polarity:
# remove cols: MEAN_SENT_POLARITY,MEAN_SENT_CATG
ts_data = ts_data[['MEAN_SENT_POLARITY']]
plot = ts_data.plot(kind='line', title="Timeseries of Twitter Sentiment Polarity")
plot.set_ylabel("SENTIMENT_POLARITY")

# plot TS of polarity:
