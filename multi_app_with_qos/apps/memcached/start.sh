#!/bin/bash

#DATA_DIR=$1

MEMCACHED_DIR="/p/lscratche/${USER}/apps/memcached/install"

${MEMCACHED_DIR}/bin/memcached -d -m 1024 -u root -l 127.0.0.1 -p 11211
