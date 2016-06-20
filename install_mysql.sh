#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
#MYSQLDIR=$APPS_DIR/mysql-5.1.57
MYSQLDIR=$APPS_DIR/mysql-5.7.9_install
#YCSBDIR=$APPS_DIR/YCSB

#if [ ! -d "$MYSQLDIR" ]; then
#    # Control will enter here if $MYSQLDIR doesn't exist.
#    echo "Error: MySQL missing"
#    exit 1
#fi

CWD=`pwd`

YCSBDIR="${APPS_DIR}/ycsb-0.4.0"

#if [ ! -d "${YCSBDIR}" ]; then
#    wget http://github.com/brianfrankcooper/YCSB/releases/download/0.4.0/ycsb-0.4.0.tar.gz
#    tar -C "${APPS_DIR}" -zxvf ycsb-0.4.0.tar.gz
#    if [ $? -ne 0 ]; then
#        echo "Error: Failed to untar YCSB"
#        exit 1
#    fi
#    rm ycsb-0.4.0.tar.gz
#fi

if [ ! -d "${MYSQLDIR}" ]; then
    echo "Installing MySQL at $MYSQLDIR"
    #tar -C "${APPS_DIR}" -zxvf mysql-5.1.57.tar.gz 
    #tar -C "${APPS_DIR}" -zxvf mysql-5.7.9.tar.gz 
    tar -C "${APPS_DIR}" -zxvf mysql-5.7.10-linux-glibc2.5-x86_64.tar.gz 
    if [ $? -ne 0 ]; then
        echo "Error: Failed to untar MySQL"
        exit 1
    fi
    cd $APPS_DIR/mysql-5.7.9/
    #mkdir -p $MYSQLDIR
    #cd $MYSQLDIR
    #cmake -DDOWNLOAD_BOOST=1 -DWITH_BOOST=$APPS_DIR/boost $APPS_DIR/mysql-5.7.9/
    #./configure --prefix=$MYSQLDIR
    #make
    #make install DESTDIR=$MYSQLDIR

    MYSQLDATADIR=/tmp/MySQLdata
    MYSQLCONFIGDIR=/tmp/MySQLetc

    #mkdir -p $MYSQLDIR
    #mkdir -p $MYSQLDATADIR
    #mkdir -p $MYSQLCONFIGDIR

    #cmake -DDOWNLOAD_BOOST=1 -DWITH_BOOST=$APPS_DIR/boost -D MYSQL_DATADIR=$MYSQLDATADIR -D SYSCONFDIR=$MYSQLCONFIGDIR -D CMAKE_INSTALL_PREFIX=$MYSQLDIR .
    #make
    #make install

fi

