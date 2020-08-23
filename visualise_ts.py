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
ts_data = ts_data[ts_data['DATE_TIME'].str.contains('2020-03|2020-04|2020-05|2020-06|2020-07')]

# get results:
results_ma1 = pd.read_csv(r"./moving_avg_results_1.csv")
results_ma5 = pd.read_csv(r"./moving_avg_results_5.csv")

# final results: WMA and SMA
final_results_w = pd.read_csv(r"./output/job_4/part-00000.csv")
final_results_w = final_results_w[final_results_w['DATE_TIME'].str.contains('2020-07')]
#final_results_w = final_results_w[final_results_w['DATE_TIME'].str.contains('2020-03|2020-04|2020-05|2020-06|2020-07')]
final_results_w = final_results_w[['DATE_TIME', 'MEAN_SENT_CATG', 'WMA_3', 'WMA_5', 'WMA_10']]

final_results_s = pd.read_csv(r"./output/job_3/part-00000.csv")
final_results_s = final_results_s[final_results_s['DATE_TIME'].str.contains('2020-07')]
#final_results_s = final_results_s[final_results_s['DATE_TIME'].str.contains('2020-03|2020-04|2020-05|2020-06|2020-07')]
final_results_s = final_results_s[['DATE_TIME', 'MEAN_SENT_CATG', 'SMA_3', 'SMA_5', 'SMA_10']]

###########################################
# adjust data
###########################################

# Set datetime column:
format = '%Y-%m-%d %H'
ts_data['DATE_TIME'] = pd.to_datetime(ts_data['DATE_TIME'], format=format)
ts_data = ts_data.set_index(pd.DatetimeIndex(ts_data['DATE_TIME']))

# adjust cols:
final_results_w['DATE_TIME'] = pd.to_datetime(final_results_w['DATE_TIME'], format=format)
final_results_w = final_results_w.set_index(pd.DatetimeIndex(final_results_w['DATE_TIME']))
final_results_w['WMA_3'] = [float(i) for i in final_results_w['WMA_3']]
final_results_w['WMA_5'] = [float(i) for i in final_results_w['WMA_5']]
final_results_w['WMA_10'] = [float(i) for i in final_results_w['WMA_10']]

final_results_s['DATE_TIME'] = pd.to_datetime(final_results_s['DATE_TIME'], format=format)
final_results_s = final_results_s.set_index(pd.DatetimeIndex(final_results_s['DATE_TIME']))
final_results_s['SMA_3'] = [float(i) for i in final_results_s['SMA_3']]
final_results_s['SMA_5'] = [float(i) for i in final_results_s['SMA_5']]
final_results_s['SMA_10'] = [float(i) for i in final_results_s['SMA_10']]

# find lowest error across all:
results_ma1['TOTAL'] = results_ma1['MSE']+results_ma1['RMSE']+results_ma1['MAE']
results_ma5['TOTAL'] = results_ma5['MSE']+results_ma5['RMSE']+results_ma5['MAE']

###########################################
# Plot:
###########################################

# plot TS of polarity:
# remove cols: MEAN_SENT_POLARITY,MEAN_SENT_CATG
ts_data1 = ts_data[['MEAN_SENT_POLARITY']]
plot = ts_data1.plot(kind='line', title="Timeseries of Twitter Sentiment Polarity")
plot.set_ylabel("SENTIMENT_POLARITY")

# plot distribution of tweets over time:
ts_data2 = ts_data[['TWEETS_PER_HOUR']]
plot2 = ts_data2.plot(kind='line', title="Distribution of Tweets per Hour")
plot2.set_ylabel("TWEETS_PER_HOUR")

# plot WMA models:
plot3 = final_results_w[['MEAN_SENT_CATG','WMA_3', 'WMA_5', 'WMA_10']].plot(kind='line', title="WMA Results - 1 Month")
plot3.set_ylabel("MEAN_SENTIMENT")

# plot SMA models:
plot4 = final_results_s[['MEAN_SENT_CATG','SMA_3', 'SMA_5', 'SMA_10']].plot(kind='line', title="SMA Results - 1 Month")
plot4.set_ylabel("MEAN_SENTIMENT")


