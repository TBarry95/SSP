############################################
# DES: Reading in results from sentiment analysis performed using
#      Hadoop MapReduce, this script uses the aggregated data to predict
#      hourly sentiment based on the occurence of COVID in tweets.
# BY: Tiernan Barry
###########################################

import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import MinMaxScaler
from pyspark.sql import SparkSession
import re
from pyspark.ml.evaluation import RegressionEvaluator
import pandas as pd

###########################################
# Get data
###########################################

spark = SparkSession.builder.appName("covid_prediction").getOrCreate()
covid_count =  spark.read.option("header", "true").csv("s3://tbarry-ssp-project/output/job_2/part-00000.csv")
df_covid_count = covid_count.select("*").toPandas()

###########################################
# Clean data
###########################################

# columns
df_covid_count.columns = ['DATE_TIME', 'SOURCE', 'MEAN_SENT_POLARITY', 'MEAN_SENT_CATG',
                        'STND_DEV_SENT', 'MEDIAN_SENT', 'MIN_SENT', 'MAX_SENT',
                        'FAVS_PER_TWEET', 'RT_PER_TWEET', 'CORR_FAV_SENT', 'CORR_RT_SENT',
                        'TWEETS_PER_HOUR', 'COVID_COUNT']

df_covid_count = df_covid_count[['DATE_TIME','MEAN_SENT_POLARITY', 'MEAN_SENT_CATG', 'TWEETS_PER_HOUR']]
df_covid_count["MEAN_SENT_POLARITY"] = [float(i) for i in df_covid_count["MEAN_SENT_POLARITY"]]
df_covid_count["MEAN_SENT_CATG"] = [float(i) for i in df_covid_count["MEAN_SENT_CATG"]]
df_covid_count["TWEETS_PER_HOUR"] = [int(i) for i in df_covid_count["TWEETS_PER_HOUR"]]

# remove before Feb 2020
filter_date = '2020-02|2020-03|2020-04|2020-05|2020-06|2020-07|2020-08|2020-09'
df_covid_count = df_covid_count[df_covid_count['DATE_TIME'].str.contains(filter_date)]
print("Number of rows after removing before 2020:", len(df_covid_count))

# ensure enough tweets per hour:
df_covid_count = df_covid_count[df_covid_count['TWEETS_PER_HOUR'] > 10]
print("Number of rows with > 10 tweets an hour:", len(df_covid_count))
#print(df_covid_count.head())

# save date for later
date = df_covid_count["DATE_TIME"]
del df_covid_count["DATE_TIME"]
#print(df_covid_count.head())

###########################################
# Make DF: Data, sent, sent -1
###########################################

#print(df_covid_count.head())
#print(df_covid_count.tail())

shifted_sentiment = df_covid_count['MEAN_SENT_CATG'].shift(1)
sentiment = df_covid_count['MEAN_SENT_CATG']

df_sentiment = pd.DataFrame()
df_sentiment['MEAN_SENT_CATG'] = sentiment
df_sentiment['MEAN_SENT_CATG_SHIFT'] = shifted_sentiment

print(df_sentiment.head())
print(df_sentiment.tail())

df_sentiment = df_sentiment.dropna()

###########################################
# Prepare spark model:
###########################################

df_clean = spark.createDataFrame(df_sentiment)
assembler = VectorAssembler().setInputCols(["MEAN_SENT_CATG_SHIFT"]).setOutputCol("IND_VARS")
df_clean_assmbl  = assembler.transform(df_clean)
df_clean_assmbl = df_clean_assmbl.select(['IND_VARS', 'MEAN_SENT_CATG'])
df_clean_assmbl.show(3)

# split data
splits = df_clean_assmbl.randomSplit([0.7, 0.3],1)
df_train  = splits[0]
df_test  = splits[1]

# LR model:
lr = LinearRegression(featuresCol = "IND_VARS",
                        labelCol="MEAN_SENT_CATG",
                        maxIter=10,
                        regParam=0.3,
                        elasticNetParam=0.8)
lr_model = lr.fit(df_train)

# summary
print("Predictors: ", "MEAN_SENT_CATG_SHIFT")
print("Coefficients: " + str(lr_model.coefficients))
print("Intercept: " + str(lr_model.intercept))
train_summary = lr_model.summary
print("RMSE: %f" % train_summary.rootMeanSquaredError)
print("r2: %f" % train_summary.r2)

lr_predictions = lr_model.transform(df_test)
lr_predictions.select("prediction","MEAN_SENT_CATG","IND_VARS").show(5)

lr_evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="MEAN_SENT_CATG", metricName="r2")
print("R Squared (R2) on test data = %g" % lr_evaluator.evaluate(lr_predictions))

# test
test_result = lr_model.evaluate(df_test)
print("Root Mean Squared Error (RMSE) on test data = %g" % test_result.rootMeanSquaredError)

predictions = lr_model.transform(df_test)
predictions.select("prediction","MEAN_SENT_CATG","IND_VARS").show()

