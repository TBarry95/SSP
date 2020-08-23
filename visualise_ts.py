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

ts_data = pd.read_csv(r"./output/job_2/part-00000.csv")
ts_data = ts_data[ts_data['DATE_TIME'].str.contains('2020')]

###########################################
# Set datetime column:
###########################################

format = '%Y-%m-%d %H'
ts_data['DATE_TIME'] = pd.to_datetime(ts_data['DATE_TIME'], format=format)
ts_data = ts_data.set_index(pd.DatetimeIndex(ts_data['DATE_TIME']))

# remove cols: MEAN_SENT_POLARITY,MEAN_SENT_CATG
ts_data = ts_data[['MEAN_SENT_POLARITY', 'MEAN_SENT_CATG']]

###########################################
# Plot:
###########################################

plot = ts_data.plot(kind='line')

