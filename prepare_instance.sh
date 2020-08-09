# !/bin/bash

##############################################
# DES: Once AWS launches, run this shell script to 
#      prepare the instance.
##############################################

sudo yum update

sudo yum install git

git clone https://github.com/TBarry95/SSP

pip3 install --user pandas

pip3 install --user findspark

