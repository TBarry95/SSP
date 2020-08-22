######################################################
# DES: Read results from S3 and provide summary accuracy measures
#      - Predcitions from SMA and WMA
# BY: Tiernan BArry
######################################################

######################################################
# Libraries:
######################################################

import pandas as pd
import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
import re
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import statistics
import math

######################################################
# Get data:
######################################################

spark = SparkSession.builder.appName("sentiment_pred_results").getOrCreate()
sma_data = spark.read.option("header", "true").csv("s3://tbarry-ssp-project/output/job_3/part-00000.csv")
wma_data = spark.read.option("header", "true").csv("s3://tbarry-ssp-project/output/job_4/part-00000.csv")
df_sma = sma_data.select("*").toPandas()
df_wma = wma_data.select("*").toPandas()
#print(df_sma.head())

###########################################
# Clean data
###########################################

#DATE_TIME,MEAN_SENT_CATG,SMA_3,SMA_5,SMA_10,SMA_3_ERROR,SMA_5_ERROR,SMA_10_ERROR
# columns
df_sma.columns = ['DATE_TIME','MEAN_SENT_CATG','SMA_3','SMA_5','SMA_10','SMA_3_ERROR','SMA_5_ERROR','SMA_10_ERROR']
df_wma.columns = ['DATE_TIME','MEAN_SENT_CATG','WMA_3','WMA_5','WMA_10','WMA_3_ERROR','WMA_5_ERROR','WMA_10_ERROR']
#print(df_sma.head())

df_sma = df_sma[df_sma['SMA_10'].notnull()]
df_wma = df_wma[df_wma['WMA_10'].notnull()]
df_sma = df_sma[df_sma['SMA_10'] != 'None']
df_wma = df_wma[df_wma['WMA_10'] != 'None']
#print(df_wma.head())

# Multiple by 100 to normalise data
df_sma["MEAN_SENT_CATG"] = [float(i)*100 for i in df_sma["MEAN_SENT_CATG"]]
df_sma["SMA_3"] = [float(i)*100 for i in df_sma["SMA_3"]]
df_sma["SMA_5"] = [float(i)*100 for i in df_sma["SMA_5"]]
df_sma["SMA_10"] = [float(i)*100 for i in df_sma["SMA_10"]]
df_sma["SMA_3_ERROR"] = [float(i)*100 for i in df_sma["SMA_3_ERROR"]]
df_sma["SMA_5_ERROR"] = [float(i)*100 for i in df_sma["SMA_5_ERROR"]]
df_sma["SMA_10_ERROR"] = [float(i)*100 for i in df_sma["SMA_10_ERROR"]]

df_wma["MEAN_SENT_CATG"] = [float(i)*100 for i in df_wma["MEAN_SENT_CATG"]]
df_wma["WMA_3"] = [float(i)*100 for i in df_wma["WMA_3"]]
df_wma["WMA_5"] = [float(i)*100 for i in df_wma["WMA_5"]]
df_wma["WMA_10"] = [float(i)*100 for i in df_wma["WMA_10"]]
df_wma["WMA_3_ERROR"] = [float(i)*100 for i in df_wma["WMA_3_ERROR"]]
df_wma["WMA_5_ERROR"] = [float(i)*100 for i in df_wma["WMA_5_ERROR"]]
df_wma["WMA_10_ERROR"] = [float(i)*100 for i in df_wma["WMA_10_ERROR"]]
#print(df_sma.head())

###########################################
# Get last month:
###########################################

# remove before Feb 2020
df_sma_jul = df_sma[df_sma['DATE_TIME'].str.contains('2020-07')]
df_wma_jul = df_wma[df_wma['DATE_TIME'].str.contains('2020-07')]
#print(df_sma_jul)
#print(df_wma_jul)

###########################################
# Get accuracy statistics:
###########################################

################################
# MSE:
################################

# SMA
mse_sma3 = mean_squared_error(df_sma_jul['MEAN_SENT_CATG'], df_sma_jul['SMA_3'])
print("MSE 3-hour SMA: ", mse_sma3)
mse_sma5 = mean_squared_error(df_sma_jul['MEAN_SENT_CATG'], df_sma_jul['SMA_5'])
print("MSE 5-hour SMA: ", mse_sma5)
mse_sma10 = mean_squared_error(df_sma_jul['MEAN_SENT_CATG'], df_sma_jul['SMA_10'])
print("MSE 10-hour SMA: ", mse_sma10)

# WMA:
mse_wma3 = mean_squared_error(df_wma_jul['MEAN_SENT_CATG'], df_wma_jul['WMA_3'])
print("MSE 3-hour WMA: ", mse_wma3)
mse_wma5 = mean_squared_error(df_wma_jul['MEAN_SENT_CATG'], df_wma_jul['WMA_5'])
print("MSE 5-hour WMA: ", mse_wma5)
mse_wma10 = mean_squared_error(df_wma_jul['MEAN_SENT_CATG'], df_wma_jul['WMA_10'])
print("MSE 10-hour WMA: ", mse_wma10)

################################
# RMSE:
################################

print("RMSE 3-hour SMA: ", math.sqrt(mse_sma3))
print("RMSE 5-hour SMA: ", math.sqrt(mse_sma5))
print("RMSE 10-hour SMA: ", math.sqrt(mse_sma10))

print("RMSE 3-hour WMA: ", math.sqrt(mse_wma3))
print("RMSE 5-hour WMA: ", math.sqrt(mse_wma5))
print("RMSE 10-hour WMA: ", math.sqrt(mse_wma10))

################################
# MAE:
################################

# SMA:
mae_sma3 = mean_absolute_error(df_sma_jul['MEAN_SENT_CATG'], df_sma_jul['SMA_3'])
print("MAE 3-hour SMA: ", mae_sma3)
mae_sma5 = mean_absolute_error(df_sma_jul['MEAN_SENT_CATG'], df_sma_jul['SMA_5'])
print("MAE 5-hour SMA: ", mae_sma5)
mae_sma10 = mean_absolute_error(df_sma_jul['MEAN_SENT_CATG'], df_sma_jul['SMA_10'])
print("MAE 10-hour SMA: ", mae_sma10)

# WMA:
mae_wma3 = mean_absolute_error(df_wma_jul['MEAN_SENT_CATG'], df_wma_jul['WMA_3'])
print("MAE 3-hour WMA: ", mae_wma3)
mae_wma5 = mean_absolute_error(df_wma_jul['MEAN_SENT_CATG'], df_wma_jul['WMA_5'])
print("MAE 5-hour WMA: ", mae_wma5)
mae_wma10 = mean_absolute_error(df_wma_jul['MEAN_SENT_CATG'], df_wma_jul['WMA_10'])
print("MAE 10-hour WMA: ", mae_wma10)

###########################################
# Table of statistics:
###########################################

df_results = pd.DataFrame()
df_results['MODEL'] = ["SMA_3", "SMA_5","SMA_10","WMA_3","WMA_5","WMA_10"]
df_results['MSE'] = [mse_sma3, mse_sma5, mse_sma10, mse_wma3, mse_wma5, mse_wma10]
df_results['RMSE'] = [math.sqrt(mse_sma3), math.sqrt(mse_sma5),math.sqrt(mse_sma10), math.sqrt(mse_wma3), math.sqrt(mse_wma5), math.sqrt(mse_wma10)]
df_results['MAE'] = [mae_sma3, mae_sma5, mae_sma10, mae_wma3, mae_wma5, mae_wma10]
print(df_results)

df_results.to_csv(r"/home/hadoop/SSP/moving_avg_results.csv", index=True)
