#!/bin/bash

NGINX_DIR="/p/lscratche/${USER}/apps/nginx-1.8.0"

$NGINX_DIR/sbin/nginx -c conf/nginx_non_root.conf
