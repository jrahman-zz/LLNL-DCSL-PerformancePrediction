#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
CWD=`pwd`

#wget http://ftp.heanet.ie/mirrors/www.apache.org/dist/maven/maven-3/3.2.1/binaries/apache-maven-3.2.1-bin.tar.gz
wget https://www.apache.org/dist/maven/binaries/apache-maven-3.2.1-bin.tar.gz
tar xzf apache-maven-*-bin.tar.gz -C $APPS_DIR
ln -s "${APPS_DIR}/apache-maven"-*/bin/mvn "${CWD}/mvn"


