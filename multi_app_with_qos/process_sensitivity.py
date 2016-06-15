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

import util
from sklearn.isotonic import IsotonicRegression

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

def process_perf(experiment_name, input_file):
    #input_file = "/home/mitra4/work/scheduling_work/LLNL-DCSL-PerformancePrediction/multi_app_with_qos/" + input_file
    #experiment_name = "./" + experiment_name
    #print experiment_name, input_file
    #processFile = "/home/mitra4/work/scheduling_work/LLNL-DCSL-PerformancePrediction/processing/process_perf.py"
    subprocess.check_call(['../processing/process_perf.py', experiment_name, input_file])
    #subprocess.check_call([processFile, experiment_name, input_file], shell=True)
    #cmd = processFile + " " + experiment_name + " " + input_file
    #os.system(cmd)

def mean_timeseries(path):
    val = subprocess.check_output(['../processing/average_timeseries.py', path, 'mean']).decode('utf-8').strip()
    #print "Received val: ", val
    f_val = float(val)
    return f_val

def median_timeseries(path):
    val = subprocess.check_output(['../processing/average_timeseries.py', path, 'median']).decode('utf-8').strip()
    #print "Received val: ", val
    f_val = float(val)
    return f_val

def ninetyfifth_timeseries(path):
    val = subprocess.check_output(['../processing/average_timeseries.py', path, '95th']).decode('utf-8').strip()
    #print "Received val: ", val
    f_val = float(val)
    return f_val

def get_mean_ipc(path):
    process_perf('tmp_exp', path)
    #return mean_timeseries('tmp_exp.ipc')
    return ninetyfifth_timeseries('tmp_exp.ipc')

def read_filelist(directory):
    data_points = []
    ycsb_apps = set(['mongodb', 'mysql', 'memcached', 'redis'])
    files = subprocess.check_output(['ls', '-1', directory]).decode('utf-8').split('\n')
    for f in files:
        try:
            app, bubble_size, rep, ftype = f.strip().split('.')
            data_points.append({
                'qos_app': app,
                'bubble_size': int(bubble_size),
                'rep': int(rep),
                'type': ftype,
                'file': '%(directory)s/' % locals() + f.strip(),
                'driver': 'ycsb'
            })
            if data_points[-1]['qos_app'] not in ycsb_apps:
                data_points[-1]['driver'] = 'ab'
        except Exception as e:
            pass
    return data_points

def build_curves(data, filename):
    
    curves = dict()

    # Key contains qos_app-metric pairs
    for key, group in data.groupby('key', sort=False):
        qos_app, metric = key.split('-')
        if qos_app not in curves:
            curves[qos_app] = dict()
        g = group.sort_values('bubble_size_kb')
        x = g['bubble_size_kb']
        y = g['value']
        low = y.idxmin()
        high = y.idxmax()
        if x[low] < x[high]:
            increasing = True
            base_value = y[low]
        else:
            increasing = False
            base_value = y[high]
        curve = IsotonicRegression(increasing=increasing)
        curve.fit(x, y)
        curves[qos_app][metric] = (curve, base_value)

    with open(filename, 'w') as f:
        pickle.dump(curves, f, pickle.HIGHEST_PROTOCOL)
    return curves
    
def plot_curves(data, curves):
    for level, group in data.groupby('key'):
        #d = group.sort('bubble_size_kb')
        d = group.sort_values('bubble_size_kb')
        sns.pointplot(data=d, estimator=np.median, y='value', x='bubble_size_kb', join=True)
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=45)
        plt.ylabel(level)
        plt.xlabel('Bubble Size (KB)')
        plt.legend()
        plt.savefig(level + '.png')
        plt.close()

def dump_sensitivity_data(data):
     for key, group in data.groupby('key', sort=False):
        qos_app, metric = key.split('-')
     	fname = qos_app + "_curve.bubble_size.ipc"
        g = group.sort_values('bubble_size_kb')
        x = g['bubble_size_kb']
        y = g['value']

        with open(fname, 'w') as f:
          writer = csv.writer(f, delimiter=' ')
          writer.writerows(zip(x,y))

def process_sensitivity(filename):
    data_points = read_filelist('sensitivity_data')
    data = {'key': [], 'qos_app': [], 'bubble_size_kb': [], 'metric': [], 'rep': [], 'value': []}
    for data_point in data_points:
        if data_point['type'] == 'driver':
	    # subrata 6/13/2016: I will focus on the IPC for QoS. Hence continuing the "driver"/latency related data
            continue
            if data_point['driver'] == 'ycsb':
                metrics = util.parse_ycsb(data_point['file'])
            elif data_point['driver'] == 'ab':
                metrics = util.parse_ab(data_point['file'])
            for metric in metrics:
                data['key'].append(data_point['qos_app'] + "-" + metric)
                data['qos_app'].append(data_point['qos_app'])
                data['bubble_size_kb'].append(data_point['bubble_size'])
                data['metric'].append(metric)
                data['rep'].append(data_point['rep'])
                data['value'].append(metrics[metric])
        elif data_point['type'] == 'perf':
	    # subrata 6/13/2016: I will focus on the IPC for QoS. 	
            #continue
            mean_ipc = get_mean_ipc(data_point['file'])
            data['key'].append(data_point['qos_app'] + "-IPC")
            data['qos_app'].append(data_point['qos_app'])
            data['bubble_size_kb'].append(data_point['bubble_size'])
            data['metric'].append('IPC')
            data['rep'].append(data_point['rep'])
            data['value'].append(mean_ipc)
 
    data = pd.DataFrame(data)
   
    dump_sensitivity_data(data) 
    curves = build_curves(data, filename)
    plot_curves(data, curves)
 
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: usage process_sensitivity.py OUTPUT_FILENAME")
        sys.exit(1)
    process_sensitivity(sys.argv[1])
