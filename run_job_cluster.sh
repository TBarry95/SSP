#!/bin/bash

#############################################
# Des: This shell script is used for full automation of the SSP project.
#      The following jobs are ran:
#      - Combine batch Twitter data into single file (send to S3 and HDFS)
#      - Hadoop job 1: Clean data - map only job
#      - Hadoop job 2: Sentiment analysis - map-reduce job
#      - Hadoop job 3: Run SMA timeseries analysis - map-reduce job
#      - Hadoop job 4: Run WMA timeseries analysis - map-reduce job
#      - Run Spark 1: LR model to predict sentiment
#      - Copy output files to S3 bucket, and to Master node instance
#      - Get prediction results summary
# BY: Tiernan Barry
#############################################

#############################################
# Define working paths
#############################################

HDFS_PATH='/ssp_project'
HDUSER_PATH='/home/hadoop/SSP'
S3_PATH='s3://tbarry-ssp-project'

#############################################
# set permissions of scripts
#############################################

chmod +x $HDUSER_PATH/mapper_clean2.py
chmod +x $HDUSER_PATH/get_tweets/combine_tweets.py
chmod +x $HDUSER_PATH/mapper_sentiment.py
chmod +x $HDUSER_PATH/reducer_sentiment.py
chmod +x $HDUSER_PATH/mapper_sma.py
chmod +x $HDUSER_PATH/reducer_sma.py
chmod +x $HDUSER_PATH/reducer_wma.py

#############################################
# Run python job to create raw dataset (combines files) and send to S3
#############################################

echo "Combining raw dataset and sending to S3 for storage" 
python3 $HDUSER_PATH/get_tweets/combine_tweets.py
aws s3 cp $HDUSER_PATH/get_tweets/combined_tweets_noheader.csv $S3_PATH/input/

#############################################
# Create folder structure on HDFS and copy input files from local file system
#############################################

echo "Initialising HDFS folders if not already set up"
hdfs dfs -mkdir $HDFS_PATH
hdfs dfs -mkdir $HDFS_PATH/input

echo "Loading data to HDFS if not already present"
hdfs dfs -copyFromLocal $HDUSER_PATH/get_tweets/combined_tweets_noheader.csv $HDFS_PATH/input

#############################################
# Delete output if exists: If  the output folder already exists, hadoop fails
#############################################

echo "Initialising folders for storing Map Reduce outputs"
hdfs dfs -rm $HDFS_PATH/output_job1/*
hdfs dfs -rmdir $HDFS_PATH/output_job1
hdfs dfs -rm $HDFS_PATH/output_job2/*
hdfs dfs -rmdir $HDFS_PATH/output_job2
hdfs dfs -rm $HDFS_PATH/output_job3/*
hdfs dfs -rmdir $HDFS_PATH/output_job3
hdfs dfs -rm $HDFS_PATH/output_job4/*
hdfs dfs -rmdir $HDFS_PATH/output_job4

#############################################
# Run hadoop job 1: Clean data
#############################################

echo "Launching Hadoop Job 1: Preprocess and clean Twitter data"
hadoop jar /lib/hadoop/hadoop-streaming.jar \
-D mapred.reduce.tasks=0 \
-file $HDUSER_PATH/mapper_clean2.py \
-mapper 'python3 mapper_clean2.py' \
-input $HDFS_PATH/input/combined_tweets_noheader.csv \
-output $HDFS_PATH/output_job1

#############################################
# Run hadoop job 2: run sentiment analysis and aggregate by date
#############################################

echo "Launching Hadoop Job 2: Run sentiment analysis on tweets by hour"
hadoop jar /lib/hadoop/hadoop-streaming.jar \
-D mapred.reduce.tasks=1 \
-file $HDUSER_PATH/mapper_sentiment.py $HDUSER_PATH/reducer_sentiment.py \
-mapper 'python3 mapper_sentiment.py' \
-reducer 'python3 reducer_sentiment.py' \
-input $HDFS_PATH/output_job1/part-00000 \
-input $HDFS_PATH/output_job1/part-00001 \
-input $HDFS_PATH/output_job1/part-00002 \
-input $HDFS_PATH/output_job1/part-00003 \
-input $HDFS_PATH/output_job1/part-00004 \
-input $HDFS_PATH/output_job1/part-00005 \
-input $HDFS_PATH/output_job1/part-00006 \
-input $HDFS_PATH/output_job1/part-00007 \
-output $HDFS_PATH/output_job2

#############################################
# Run hadoop job 3: run Simple Moving averages analysis on TS sentiments
#############################################

echo "Launching Hadoop Job 3: Run Simple Moving Averages analysis on aggregated tweet sentiment"
hadoop jar /lib/hadoop/hadoop-streaming.jar \
-D mapred.reduce.tasks=1 \
-file $HDUSER_PATH/mapper_sma.py $HDUSER_PATH/reducer_sma.py \
-mapper "python3 mapper_sma.py" \
-reducer "python3 reducer_sma.py" \
-input $HDFS_PATH/output_job2/part-00000 \
-output $HDFS_PATH/output_job3

#############################################
# Run hadoop job 4: Run Weighted Moving averages analysis on TS sentiments
#############################################

echo "Launching Hadoop Job 3: Run Simple Moving Averages analysis on aggregated tweet sentiment"
hadoop jar /lib/hadoop/hadoop-streaming.jar \
-D mapred.reduce.tasks=1 \
-file $HDUSER_PATH/mapper_sma.py $HDUSER_PATH/reducer_wma.py \
-mapper "python3 mapper_sma.py" \
-reducer "python3 reducer_wma.py" \
-input $HDFS_PATH/output_job2/part-00000 \
-output $HDFS_PATH/output_job4

#############################################
# Copy output files to local file system
#############################################

echo "Copying final output from HDFS to local folder"
mkdir $HDUSER_PATH/output
rm $HDUSER_PATH/output/job_1/*
rmdir $HDUSER_PATH/output/job_1
mkdir $HDUSER_PATH/output/job_1
rm $HDUSER_PATH/output/job_2/*
rmdir $HDUSER_PATH/output/job_2
mkdir $HDUSER_PATH/output/job_2
rm $HDUSER_PATH/output/job_3/*
rmdir $HDUSER_PATH/output/job_3
mkdir $HDUSER_PATH/output/job_3
rm $HDUSER_PATH/output/job_4/*
rmdir $HDUSER_PATH/output/job_4
mkdir $HDUSER_PATH/output/job_4

hdfs dfs -copyToLocal $HDFS_PATH/output_job1/* $HDUSER_PATH/output/job_1
hdfs dfs -copyToLocal $HDFS_PATH/output_job2/* $HDUSER_PATH/output/job_2
hdfs dfs -copyToLocal $HDFS_PATH/output_job3/* $HDUSER_PATH/output/job_3
hdfs dfs -copyToLocal $HDFS_PATH/output_job4/* $HDUSER_PATH/output/job_4
mv $HDUSER_PATH/output/job_2/part-00000 $HDUSER_PATH/output/job_2/part-00000.csv
mv $HDUSER_PATH/output/job_3/part-00000 $HDUSER_PATH/output/job_3/part-00000.csv
mv $HDUSER_PATH/output/job_4/part-00000 $HDUSER_PATH/output/job_4/part-00000.csv

#############################################
# Copy output files to S3
#############################################
echo "Copying final output to S3"
aws s3 cp $HDUSER_PATH/output/job_1 $S3_PATH/output/job_1/ --recursive
aws s3 cp $HDUSER_PATH/output/job_2 $S3_PATH/output/job_2/ --recursive
aws s3 cp $HDUSER_PATH/output/job_3 $S3_PATH/output/job_3/ --recursive
aws s3 cp $HDUSER_PATH/output/job_4 $S3_PATH/output/job_4/ --recursive

# copy files back again to enable push to github (changed name to csv above)
hdfs dfs -copyToLocal $HDFS_PATH/output_job2/* $HDUSER_PATH/output/job_2
hdfs dfs -copyToLocal $HDFS_PATH/output_job3/* $HDUSER_PATH/output/job_3
hdfs dfs -copyToLocal $HDFS_PATH/output_job4/* $HDUSER_PATH/output/job_4

#############################################
# Run Spark job:
#############################################

echo "Launching Spark job: Regression analysis"
python3 $HDUSER_PATH/lr_model_spark.py

#############################################
# Get Moving Avergae Results and export to Repo:
#############################################

python3 $HDUSER_PATH/moving_avg_results.py

