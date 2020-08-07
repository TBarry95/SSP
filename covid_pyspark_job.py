################################################
# DES:
# BY: 
################################################


################################################
# Libraries:
################################################

# spark:
import findspark
findspark.init()
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark import SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession

# other:
import pandas as pd
from scipy import stats

# timeseries - spark - flint
#import ts.flint
#from ts.flint import FlintContext, summarizers
#from ts.flint import udf

################################################
# Get data from HDFS
################################################

spark = SparkSession.builder.appName("covid_prediction").getOrCreate()
covid_count =  spark.read.csv("hdfs://ip-172-31-87-203.ec2.internal:8020/ssp_project/output_job2/part-00000")

print(type(covid_count))
df_covid_count = covid_count.select("*").toPandas()
print(df_covid_count.head())

################################################
# Clean data:
################################################

df_covid_count = df_covid_count[1:]
df_covid_count.columns = ["DATE_TIME", "FAVS_COUNT", "RT_COUNT", "TWEET_COUNT", "COVID_COUNT"]
print(df_covid_count.head())

################################################
# Prepare modelling:
################################################







#sqlContext = SQLContext(spark)
#flintContext = FlintContext()
#flint_df = flintContext.read.pandas(df_covid_count)

#@udf('double')
#def rank(v):
#      return v.rank(pct=True)

#@udf('double')
#def boxcox(v):
#    return pd.Series(stats.boxcox(v)[0])


# df = covid_count.addColumnsForCycle({'rank': rank(covid_count['COVID_COUNT\t'])})

#sqlContext = SQLContext(spark)
#flintContext = FlintContext(sqlContext)

#df_flint  = flintContext.read.dataframe(df_covid_count)
#print(type(df_flint))

#master_node_url = "ec2-3-86-207-165.compute-1.amazonaws.com"
#conf = SparkConf().setAppName("predict_covid_count").setMaster("local")
#sc = SparkContext(conf=conf)
