#!/bin/bash

#/usr/apps/python3.4.2/bin/virtualenv "${HOME}/mypy34"
#if [ $? -ne 0 ]; then
#    echo "Error: Failed to install virtualenv"
#    exit 1
#fi

git clone git://github.com/kennethreitz/requests.git
if [ $? -ne 0 ]; then
    echo "Error: Failed to download the repository"
    exit 2
fi

cd requests
/usr/apps/python3.4.2/bin/python3 setup.py install --user
if [ $? -ne 0 ]; then
    echo "Error: Failed to install requests"
    cd ..
    rm -rf requests
    exit 3
fi
cd ..
rm -rf requests


