#!/usr/bin/python

import sys
import os

file1 = sys.argv[1]  

f1 = open(file1, 'r')


f1_alllines = f1.readlines()
#end for

i  = 0
for line in f1_alllines:
	line = line.strip()
	fields = line.split()
	dirname = fields[-2]
	#print dirname
	fname = dirname + ".ipc"
	if(False == os.path.isfile(fname)):
		print line
	
