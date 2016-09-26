#!/usr/bin/python

import sys

file1 = sys.argv[1]  #experiment_list
file2 = sys.argv[2]  #completed_experiments

f1 = open(file1, 'r')
f2 = open(file2, 'r')


f1_alllines = f1.readlines()
f2_alllines = f2.readlines()

f2_line_dict = {}
for line in f2_alllines:
	line = line.strip()
	f2_line_dict[line] = 1

#end for

i  = 0
for line in f1_alllines:
	line = line.strip()
	i = i + 1
	if line not in f2_line_dict.keys():
		if(i < 10600):
		  print line
		#print "No results: Line number : ", str(i), "  " , line  
		#break
