# !/bin/bash

#############################################
# Define working paths
#############################################

HADOOP_PATH='/usr/local/hadoop'
HDFS_PATH='/ssp_project'
LOCAL_PATH='/home/tiernan/PycharmProjects/SSP'
HDUSER_PATH='/home/hduser/ssp_project'

#############################################
# Start Hadoop services
#############################################

#$HADOOP_PATH/sbin/start-dfs.sh
#$HADOOP_PATH/sbin/start-yarn.sh

#############################################
# Send raw data to HDUSER user
#############################################

echo "Sending raw data to HDUSER"
cp $LOCAL_PATH/get_tweets/combined_tweets_noheader.csv $HDUSER_PATH

echo "Ensuring latest mapper and reducers are being used"
# sentiment analysis: 
rm $HDUSER_PATH/mapper_clean2.py
rm $HDUSER_PATH/mapper_sentiment.py
rm $HDUSER_PATH/reducer_sentiment.py
cp $LOCAL_PATH/mapper_clean2.py $HDUSER_PATH
cp $LOCAL_PATH/mapper_sentiment.py $HDUSER_PATH
cp $LOCAL_PATH/reducer_sentiment.py $HDUSER_PATH
# covid word count:
rm $HDUSER_PATH/mapper_clean3.py
rm $HDUSER_PATH/mapper_words.py
rm $HDUSER_PATH/reducer_words.py
cp $LOCAL_PATH/mapper_clean3.py $HDUSER_PATH
cp $LOCAL_PATH/mapper_words.py $HDUSER_PATH
cp $LOCAL_PATH/reducer_words.py $HDUSER_PATH

chmod +x $HDUSER_PATH/mapper_clean2.py
chmod +x $HDUSER_PATH/mapper_sentiment.py
chmod +x $HDUSER_PATH/reducer_sentiment.py
chmod +x $HDUSER_PATH/mapper_clean3.py
chmod +x $HDUSER_PATH/mapper_words.py
chmod +x $HDUSER_PATH/reducer_words.py

#############################################
# Create folder structure on HDFS and copy input files from local file system
#############################################

echo "Initialising HDFS folders if not already set up"
$HADOOP_PATH/bin/hdfs dfs -mkdir $HDFS_PATH
$HADOOP_PATH/bin/hdfs dfs -mkdir $HDFS_PATH/input

echo "Loading data to HDFS if not already present"
$HADOOP_PATH/bin/hdfs dfs -copyFromLocal $HDUSER_PATH/combined_tweets_noheader.csv $HDFS_PATH/input

#############################################
# Delete output if exists: If  the output folder already exists, hadoop fails
#############################################

echo "Initialising local folders for storing Map Reduce outputs"
$HADOOP_PATH/bin/hdfs dfs -rm $HDFS_PATH/output_job1/*
$HADOOP_PATH/bin/hdfs dfs -rmdir $HDFS_PATH/output_job1
$HADOOP_PATH/bin/hdfs dfs -rm $HDFS_PATH/output_job2/*
$HADOOP_PATH/bin/hdfs dfs -rmdir $HDFS_PATH/output_job2

#############################################
# Run hadoop job 1:
#############################################

# hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar

echo "Launching Hadoop Job 1: Preprocess and clean Twitter data"
mapred streaming \
-D mapred.reduce.tasks=0 \
-file $HDUSER_PATH/mapper_clean3.py \
-mapper 'python3 mapper_clean3.py' \
-input $HDFS_PATH/input/combined_tweets_noheader.csv \
-output $HDFS_PATH/output_job1

#############################################
# Run hadoop job 2:
#############################################

echo "Launching Hadoop Job 2: Aggregate the occurence of COVID in tweets"
mapred streaming \
-D mapred.reduce.tasks=1 \
-file $HDUSER_PATH/mapper_words.py $HDUSER_PATH/reducer_words.py \
-mapper 'python3 mapper_words.py' \
-reducer 'python3 reducer_words.py' \
-input $HDFS_PATH/output_job1/part-00000 \
-input $HDFS_PATH/output_job1/part-00001 \
-output $HDFS_PATH/output_job2

#############################################
# Copy output files to local file system
#############################################

echo "Copying final output from HDFS to local folder"  
rm /home/hduser/ssp_project/output/job_1/*
rmdir /home/hduser/ssp_project/output/job_1
mkdir /home/hduser/ssp_project/output/job_1

rm /home/hduser/ssp_project/output/job_2/*
rmdir /home/hduser/ssp_project/output/job_2
mkdir /home/hduser/ssp_project/output/job_2

$HADOOP_PATH/bin/hdfs dfs -copyToLocal $HDFS_PATH/output_job1/* /home/hduser/ssp_project/output/job_1
$HADOOP_PATH/bin/hdfs dfs -copyToLocal $HDFS_PATH/output_job2/* /home/hduser/ssp_project/output/job_2


#############################################
# Stop Hadoop services
#############################################

#$HADOOP_PATH/sbin/stop-yarn.sh
#$HADOOP_PATH/sbin/stop-dfs.sh


