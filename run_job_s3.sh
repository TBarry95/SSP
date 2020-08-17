# !/bin/bash

#############################################
# Define working paths
#############################################

HDFS_PATH='/ssp_project'
HDUSER_PATH='/home/hadoop/SSP'
S3_PATH='s3://x19141840/ssp-project'

#############################################
# Scripts set to executable
#############################################

# make executable
chmod +x $HDUSER_PATH/mapper_clean3.py
chmod +x $HDUSER_PATH/mapper_clean2.py

#############################################
# Run hadoop job 1:
#############################################

echo "Launching Hadoop Job 1: Preprocess and clean Twitter data"
hadoop jar /lib/hadoop/hadoop-streaming.jar \
-D mapred.reduce.tasks=0 \
-file $HDUSER_PATH/mapper_clean2.py \
-mapper 'python3 mapper_clean2.py' \
-input $S3_PATH/input/combined_tweets_noheader.csv \
-output $S3_PATH/output/output_job1

#############################################
# Run hadoop job 1:
#############################################

echo "Launching Hadoop Job 2: Aggregate the occurence of COVID in tweets"
hadoop jar /lib/hadoop/hadoop-streaming.jar \
-D mapred.reduce.tasks=1 \
-file $HDUSER_PATH/mapper_words.py $HDUSER_PATH/reducer_words.py \
-mapper 'python3 mapper_words.py' \
-reducer 'python3 reducer_words.py' \
-input $S3_PATH/output_job1/part-00000 \
-input $S3_PATH/output_job1/part-00001 \
-input $S3_PATH/output_job1/part-00002 \
-input $S3_PATH/output_job1/part-00003 \
-input $S3_PATH/output_job1/part-00004 \
-input $S3_PATH/output_job1/part-00005 \
-input $S3_PATH/output_job1/part-00006 \
-input $S3_PATH/output_job1/part-00007 \
-output $S3_PATH/output_job2

