#!/bin/bash

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

echo "Initialising local folders for storing Map Reduce outputs"
hdfs dfs -rm $HDFS_PATH/output_job1/*
hdfs dfs -rmdir $HDFS_PATH/output_job1
hdfs dfs -rm $HDFS_PATH/output_job2/*
hdfs dfs -rmdir $HDFS_PATH/output_job2

#############################################
# Run hadoop job 1:
#############################################

echo "Launching Hadoop Job 1: Preprocess and clean Twitter data"
hadoop jar /lib/hadoop/hadoop-streaming.jar \
-D mapred.reduce.tasks=0 \
-file $HDUSER_PATH/mapper_clean2.py \
-mapper 'python3 mapper_clean2.py' \
-input $HDFS_PATH/input/combined_tweets_noheader.csv \
-output $HDFS_PATH/output_job1

#############################################
# Run hadoop job 2:
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

hdfs dfs -copyToLocal $HDFS_PATH/output_job1/* $HDUSER_PATH/output/job_1
hdfs dfs -copyToLocal $HDFS_PATH/output_job2/* $HDUSER_PATH/output/job_2

#############################################
# Copy output files to S3
#############################################
echo "Copying final output to S3"
aws s3 cp $HDUSER_PATH/output/job_1 $S3_PATH/output/job_1/ --recursive
aws s3 cp $HDUSER_PATH/output/job_2 $S3_PATH/output/job_2/ --recursive
