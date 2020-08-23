# Forecasting Twitter Sentiment Time Series using Map-Reduce Programming Model.  

# Reproducing this analysis:

## Set up an AWS EMR cluster:
- Set up EMR cluster as outlined by the Procedure Document provided in Moodle (supporting material).
- for setting up the EMR cluster, you will need to use the bootstrap shell file provided in the Moodle submission. Make sure to include this file as outlined in the Pocedure document for setting up the EMR cluster. 

## Deploying this Project:

### SSH into Master Node:
- Copy the address for the Master node from EMR dashboard (Master public DNS)
- Use SSH command to connect to master node as per below example:
  - ssh -i ./keys/tbarry_emr.pem hadoop@ec2-52-91-238-63.compute-1.amazonaws.com
- If SSH is not responding, please refer to the Procedure Document provided to enable SSH through AWS. 

### Clone Github repository:
- When in master node, clone GitHub repo by running the below command:
  - git clone https://github.com/TBarry95/SSP 
  - Note: Git has already been installed during the bootstrap configuration. 

### Ensure S3 Paths are Correct:
- As per the Procedure Document provided, ensure that the S3 path loations have been adjusted according to your chosen path names in the following files:
  - SSP/run_job_cluster.sh
  - SSP/moving_avg_results.py

### From ~SSP folder, run the Shell Script: run_job_cluster.sh:
- ./run_job_cluster.sh 


