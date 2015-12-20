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
    echo "Copying custom config file for non root users"
    cp multi_app_with_qos/apps/nginx/nginx_non_root.conf $NGINXDIR/conf/nginx_non_root.conf 
    rm -rf nginx-1.8.0.tar.gz nginx-1.8.0
fi


CWD=`pwd`
