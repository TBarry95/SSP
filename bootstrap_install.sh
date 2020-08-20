#!/bin/bash -xe

#############################################
# Install packages
#############################################

sudo yum update -y
sudo yum install git -y
sudo pip3 install spacy
sudo python3 -m spacy download en_core_web_sm
sudo pip3 install pandas
sudo pip3 install textblob
sudo pip3 install scipy
sudo pip3 install sortedcontainers
sudo pip3 install findspark

git config --global user.email x19141840@student.ncirl.ie
git config --global user.name "Tiernan Barry"

