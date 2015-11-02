#!/bin/bash

APPS_DIR=/p/lscratche/mitra3/apps

wget http://ftp.heanet.ie/mirrors/www.apache.org/dist/maven/maven-3/3.1.1/binaries/apache-maven-3.1.1-bin.tar.gz
tar xzf apache-maven-*-bin.tar.gz -C $APPS_DIR
cd $APPS_DIR
ln -s apache-maven-* maven


