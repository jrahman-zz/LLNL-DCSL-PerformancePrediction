#!/bin/bash

/usr/apps/python2.7.1/bin/virtualenv ~/py27

~/py27/bin/pip install Flask
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Flask"
    exit 1
fi

~/py27/bin/pip install numpy
if [ $? -ne 0 ]; then
    echo "Error: Failed to install numyp"
    exit 2
fi

~/py27/bin/pip install pandas
if [ $? -ne 0 ]; then
    echo "Error: Failed to install pandas"
    exit 3
fi

git clone git://github.com/matplotlib/matplotlib.git
if [ $? -ne 0 ]; then
    exit 4
fi
cd matplotlib
python setup.py install
if [ $? -ne 0 ]; then
    cd ..
    rm -rf matplotlib
    exit 5
fi
cd ..
rm -rf matplotlib

~/py27/bin/pip install scipy
if [ $? -ne 0 ]; then
    exit 6
fi

~/py27/bin/pip install seaborn
if [ $? -ne 0 ]; then
    exit 7
fi

