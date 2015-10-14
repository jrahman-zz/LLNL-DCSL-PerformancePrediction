#wget bootstrap.pypa.io/get-pip.py
#if [ $? -ne 0 ]; then
#	echo "Error: Failed to download get-pip.py"
#	exit 1
#fi

#python3-3.2 get-pip.py
#if [ $? -ne 0 ]; then
#	echo "Error: Failed to install pip"
#	rm "get-pip.py"
#	exit 1
#fi

#rm "get-pip.py"


#/usr/apps/python3.4.2/bin/virtualenv ~/mypy
/usr/apps/python3.2/bin/virtualenv ~/mypy

~/mypy/bin/pip install numpy
~/mypy/bin/pip install pandas

git clone git://github.com/matplotlib/matplotlib.git
if [ $? -ne 0 ]; then
	exit 1
fi
cd matplotlib
python setup.py install
if [ $? -ne 0 ]; then
	cd ..
	rm -rf matplotlib
	exit 2
fi
cd ..
rm -rf matplotlib

~/mypy/bin/pip install scipy
if [ $? -ne 0 ]; then
	exit 3
fi
