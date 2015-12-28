#!/bin/sh

APP_DIR="/p/lscratche/${USER}/apps"

cd "${APP_DIR}"
if [ -f "redis-stable.tar.gz" ]; then
    rm "redis-stable.tar.gz"
fi

wget http://download.redis.io/redis-stable.tar.gz

if [ -d "redis-stable" ]; then
    rm -rf "redis-stable"
fi

tar xvzf redis-stable.tar.gz
cd redis-stable
make
