#!/usr/bin/env python
##!/usr/apps/python3.4.2/bin/python3

import numpy as np
import pandas as pd

import pickle
import sys
import os
import subprocess
import logging
import csv

#import util
from sklearn.isotonic import IsotonicRegression

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append('../processing')
import process_perf as pp

'''
input files:
	(1) <qos_name>.standalone_stats: qos app's stand alone statistics file
	formart : 
	<qos_app_name> "standalone_metric" mean median p95 p99
	Will be available in:  ../multi_app_with_qos/standalone_data/<qos_app_name>/ dir

        (2) <qos name>_curve.bubble_size.ipc: QoS app's sensitivity profile from which bubble size will be calculated
	Will be available in:  ../multi_app_with_qos/

	(3) colocation_prediction_file: file containing all combinations of colocations
	format :
	config app_names rep observed predicted naive_sum
	Will be available in ../modelling/ dir. This is the outout file of ./matrix_model.py
'''

useStatisticsFromStandalone="p95"
#useStatisticsFromStandalone="mean"
#useStatisticsFromStandalone="median"
#useStatisticsFromStandalone="p99"

def find_qos_workload(qos_app_name):
    path = '../multi_app_with_qos/manifest/qos'
    qos_apps = []
    with open(path, 'r') as f:
        for line in f:
            val = line.strip().split()
	    if(val[0] == qos_app_name):
		return val[1]
    return ""

def read_standalone_stat_file(qos_app_name, stat_file):
        with open(stat_file, 'r') as f:
		            line = f.readline()
			    vals = line.strip().split()
			    if(vals[0] != qos_app_name):
				    print "Error: this standalone statistics file is NOT for this qos app"
				    return -1
			    if(useStatisticsFromStandalone == "mean"):
				    return float(vals[2])
			    elif(useStatisticsFromStandalone == "median"):
				    return float(vals[3])
			    elif(useStatisticsFromStandalone == "p95"):
				    return float(vals[4])
			    elif(useStatisticsFromStandalone == "p99"):
				    return float(vals[5])
				
			    return -1

        
def calculate_bubble_size(qos_standalone, qos_policy_frac, qos_app_name):
	
	degraded_qos_ipc = float(qos_standalone * qos_policy_frac)

	sensitivity_curve = qos_app_name + "_curve.bubble_size.ipc"

        val = subprocess.check_output(['../processing/estimate_bubble.py', sensitivity_curve, str(degraded_qos_ipc)])

	corresponding_bubble_size = float(float(val)/1024.0)

	print "Effective bubbler size = ", corresponding_bubble_size

	return corresponding_bubble_size

def read_colocation_prediction_file(colocation_prediction_file):
        #df = pd.read_table(colocation_prediction_file, sep=' ', header=1)
        df = pd.read_table(colocation_prediction_file, sep=' ', header=0)
	df  = df.drop_duplicates(subset=['config', 'app_names'],keep='first')
	#print df

	return df

def get_colocations(df,predicted_column, required_bubble_size):
	selected_df = df.loc[(df[predicted_column] <= required_bubble_size) & (df['config'] != '')]
	#selected_df = df[df.predicted_column < required_bubble_size]
	#print selected_df
	return selected_df

def generateDumpDir(apps, qos_app_name, rep):
        numCores = 1
	numApps = len(apps)
        output = "data_qos_predicted/" + qos_app_name + "/" + qos_app_name + "." + str(numApps)
        for app in apps:
	       output = output + "." + app + "_" + str(numCores) + "." + rep + " " + rep 		

	return output

def calculate_average_utilization():

def parse_selection_create_exp(selected_df_model, qos_app_name, qos_workload, totalRep):
        numCores = 1
	for rep in range(totalRep):
	       for index, row in selected_df_model.iterrows():
	               app_combination = row['app_names']
                       apps = app_combination.split('.')
	               exp_line = ''
                       for app in apps:
		           sep_index = app.rfind('_')
		           bmark = app[:sep_index]
		           theApp = app[sep_index+1:]
		           #print bmark, theApp
			   exp_line = exp_line + bmark + ' ' + theApp + ' ' +  str(numCores) + ' '
		       #end for

		       qos_data_dir = generateDumpDir(apps,qos_app_name, str(rep))
		       exp_line = exp_line + qos_app_name + ' ' + qos_workload + ' ' + qos_data_dir
		       print exp_line

def find_colocation_possibilities(qos_app_name, qos_policy):
	qos_policy_frac = float(qos_policy/100.0)
	qos_standalone_stat_file = qos_app_name + ".standalone_stats"
	qos = read_standalone_stat_file(qos_app_name, qos_standalone_stat_file)
	if(qos == -1):
		return 

        required_bubble_size = calculate_bubble_size(qos,qos_policy_frac,qos_app_name)

        colocation_prediction_file = "colocation_prediction_file"
	df = read_colocation_prediction_file(colocation_prediction_file)
       
	predicted_column_name = "predicted"
	naive_sum_column_name = "naive_sum"
	
	selected_df_model = get_colocations(df,predicted_column_name, required_bubble_size)
	selected_df_naive_sum = get_colocations(df,naive_sum_column_name, required_bubble_size)

	#print selected_df_model
        qos_workload = find_qos_workload(qos_app_name)
        if(qos_workload == ""):
		print "Error: No QoS app workload found"
		sys.exit(1)

	number_of_exp_repetitions = 10
        
	parse_selection_create_exp(selected_df_model, qos_app_name, qos_workload, number_of_exp_repetitions)
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
	    print("Error: usage find_colocation_possibilities.py qos_app_name qos-policy(a number:e.g. 99, 95, 90 etc.)")
            sys.exit(1)
    find_colocation_possibilities(sys.argv[1], int(sys.argv[2]))
