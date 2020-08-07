############################################
# DES: 
# BY: 
###########################################

import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
import re

###########################################
# Get data
###########################################

spark = SparkSession.builder.appName("covid_prediction").getOrCreate()
covid_count =  spark.read.csv("hdfs://ip-172-31-87-203.ec2.internal:8020/ssp_project/output_job2/part-00000")
df_covid_count = covid_count.select("*").toPandas()

###########################################
# Clean data
###########################################

# columns
df_covid_count = df_covid_count[1:]
df_covid_count.columns = ["DATE_TIME", "FAVS_COUNT", "RT_COUNT", "TWEET_COUNT", "COVID_COUNT"]
df_covid_count["FAVS_COUNT"] = [int(i) for i in df_covid_count["FAVS_COUNT"]]
df_covid_count["RT_COUNT"] = [int(i) for i in df_covid_count["RT_COUNT"]]
df_covid_count["TWEET_COUNT"] = [int(i) for i in df_covid_count["TWEET_COUNT"]]
df_covid_count["COVID_COUNT"] = [int(i) for i in df_covid_count["COVID_COUNT"]]

# remove before 2020
df_covid_count = df_covid_count[df_covid_count['DATE_TIME'].str.contains('2020')]

# save data for later
date = df_covid_count["DATE_TIME"]
del df_covid_count["DATE_TIME"]

###########################################
# Prepare spark model:
###########################################

df_clean = spark.createDataFrame(df_covid_count)

assembler = VectorAssembler(
    inputCols = ["FAVS_COUNT", "RT_COUNT", "TWEET_COUNT"],
    outputCol = "IND_VARS" )
df_clean_assmbl  = assembler.transform(df_clean)
df_clean_assmbl = df_clean_assmbl.select(["IND_VARS", "COVID_COUNT"])
df_clean_assmbl.show(3)

# split data
splits = df_clean_assmbl.randomSplit([0.7, 0.3])
df_train  = splits[0]
df_test  = splits[1]

# LR model:
lr = LinearRegression(featuresCol = "IND_VARS",
			labelCol="COVID_COUNT",
			maxIter=10,
			regParam=0.3,
			elasticNetParam=0.8)

lr_model = lr.fit(df_train)
print("Predictors: " + "FAVS_COUNT," + "RT_COUNT," + "TWEET_COUNT")
print("Coefficients: " + str(lr_model.coefficients))
print("Intercept: " + str(lr_model.intercept))





