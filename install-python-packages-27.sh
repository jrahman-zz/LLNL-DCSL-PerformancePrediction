#!/bin/bash

/usr/apps/python2.7.1/bin/virtualenv ~/py271

~/py271/bin/pip install Flask
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Flask"
    exit 1
fi

~/py271/bin/pip install 'numpy>1.7.0'
if [ $? -ne 0 ]; then
    echo "Error: Failed to install numyp"
    exit 2
fi

~/py271/bin/pip install pandas
if [ $? -ne 0 ]; then
    echo "Error: Failed to install pandas"
    exit 3
fi

git clone git://github.com/matplotlib/matplotlib.git
if [ $? -ne 0 ]; then
    exit 4
fi
cd matplotlib
~/py271/bin/python setup.py install
if [ $? -ne 0 ]; then
    cd ..
    rm -rf matplotlib
    exit 5
fi
cd ..
rm -rf matplotlib

~/py271/bin/pip install scipy
if [ $? -ne 0 ]; then
    exit 6
fi

~/py271/bin/pip install seaborn
if [ $? -ne 0 ]; then
    exit 7
fi

~/py271/bin/pip install scikit-learn
if [ $? -ne 0 ]; then
    exit 7
fi

