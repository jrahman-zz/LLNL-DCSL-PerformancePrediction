#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
NGINXDIR=$APPS_DIR/nginx-1.8.0
APACHE_BENCHDIR=$APPS_DIR/AB

if [ ! -d "$NGINXDIR" ]; then
    # Control will enter here if $NGINXDIR doesn't exist.
    mkdir -p $NGINXDIR
    echo "NGINX will be installed in : $NGINXDIR"
    wget http://nginx.org/download/nginx-1.8.0.tar.gz
    tar xvzf nginx-1.8.0.tar.gz
    cd nginx-1.8.0
    ./configure --prefix=$NGINXDIR
    make
    make install
    echo "Installation of NGINX done"
    cd ..
    rm -rf nginx-1.8.0.tar.gz nginx-1.8.0
fi


CWD=`pwd`
exit 1

YCSBDIR="${APPS_DIR}/ycsb-0.3.1"
if [ ! -d "${YCSBDIR}" ]; then
    wget http://github.com/brianfrankcooper/YCSB/releases/download/0.3.1/ycsb-0.3.1.tar.gz
    tar -C "${APPS_DIR}" -zxvf ycsb-0.3.1.tar.gz
    if [ $? -ne 0 ]; then
        echo "Error: Failed to untar YCSB"
        exit 1
    fi
    rm ycsb-0.3.1.tar.gz
fi

#if [ ! -d "$YCSBDIR" ]; then
	  # Control will enter here if $YCSBDIR doesn't exist.
#	  cd $APPS_DIR
#	  git clone git://github.com/brianfrankcooper/YCSB.git
#	  cd YCSB
#	  "${CWD}/mvn" -pl \!cassandra2,\!gemfire,\!hbase094,\!hbase098,\!hbase10,\!kudu,\!distribution clean package 
#fi
