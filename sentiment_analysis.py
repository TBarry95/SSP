############################################
# DES: Taking the results from hadoop streaming job 2, predict COVID word counts
# BY: Tiernan Barry
###########################################

import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.sql import SparkSession
import re
from pyspark.ml.evaluation import RegressionEvaluator
from textblob import TextBlob

###########################################
# Get data
###########################################

spark = SparkSession.builder.appName("sentiment_analysis").getOrCreate()
output =  spark.read.csv("hdfs://ip-172-31-95-26.ec2.internal:8020/ssp_project/output_job1/*")
df_tweets = output.select("*").toPandas()

###########################################
# Clean data: Tokenise words  
###########################################

# Fix column names
df_tweets.columns = ["date_time", "tweet_id", "source", "str_id",
               "fav_count", "rt_count", "followers", "tweet_count", "reply_ind",
               "reply_user_id", "len_tweet", "processed_text", "processed_hashtag"]

# tokenise tweets:
tokenizer = Tokenizer(outputCol="processed_tokens")
tokenizer.setInputCol("processed_text")
df_spark = spark.createDataFrame(df_tweets)
df_spark = tokenizer.transform(df_spark)
print(df_spark.show(5))

# remove stopwords:
remove_sw = StopWordsRemover(inputCol= 'processed_tokens', outputCol= 'cleaned_tweets')
df_spark = remove_sw.transform(df_spark)
print(df_spark.show(5))

###########################################
# Get Sentiment per tweet:
###########################################

df_spark_sent = df_spark.withColumn('sentiment', Textblob(df_spark).sentiment)
#sample3 = sample.withColumn('age2', sample.age + 2)
print(df_spark_sent.show(5))

###########################################
# Aggregate by date:
###########################################



###########################################
# 
###########################################
