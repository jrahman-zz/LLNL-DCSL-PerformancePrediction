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

sys.path.append('../processing')
import process_perf as pp

def process_perf_file(input_file):
    #print pp
    with open(input_file, 'r') as f:
	            (ips, ipc) = pp.process_perf(f)
    return ipc
    #subprocess.check_call(['../processing/process_perf.py', experiment_name, input_file])

def mean_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, 'mean']))

def median_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, 'median']))

def p99_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, '99th']))

def p95_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, '95th']))

def read_filelist(directory,qos_app_name):
    data_points = []
    ycsb_apps = set(['mongodb', 'mysql', 'memcached', 'redis'])
    files = subprocess.check_output(['ls', '-1', directory]).decode('utf-8').split('\n')
    for f in files:
        try:
            app, bubble_size, rep, ftype = f.strip().split('.')
	    if(app != qos_app_name):
                 continue
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


def dump_merged_standalone_data(ipc, dumpFileName):
    with open(dumpFileName, 'w') as ipc_f:
     times = sorted(ipc.keys())
     for time in times:
        ipc_f.write('%f %f\n' % (time, ipc[time]))


def process_sensitivity(qos_app_name):
    dataDirName = 'standalone_data/%(qos_app_name)s' % locals()
    data_points = read_filelist(dataDirName, qos_app_name)
    data = {'key': [], 'qos_app': [], 'bubble_size_kb': [], 'metric': [], 'rep': [], 'value': []}

    ipcs_from_all_reps = {}
    for data_point in data_points:
        if data_point['type'] == 'driver':
        # subrata 6/13/2016: I will focus on the IPC for QoS. Hence continuing the "driver"/latency related data
            continue
        elif data_point['type'] == 'perf':
        # subrata 6/13/2016: I will focus on the IPC for QoS. 
            #continue
            #mean_ipc = get_mean_ipc(data_point['file'])
	    ipc = process_perf_file(data_point['file'])
	    ipcs_from_all_reps.update(ipc)
  
    merged_IPC_file_name = dataDirName + '/merged_ipc_standalone_reps.ipc' 
    
    dump_merged_standalone_data(ipcs_from_all_reps, merged_IPC_file_name)

    meanIPC = mean_timeseries(merged_IPC_file_name)
    medianIPC = median_timeseries(merged_IPC_file_name)
    p95IPC = p95_timeseries(merged_IPC_file_name)
    p99IPC = p99_timeseries(merged_IPC_file_name)

    stats_to_print = '%(qos_app_name)s standalone_metric %(meanIPC)s %(medianIPC)s %(p95IPC)s %(p99IPC)s' % locals()
    print stats_to_print

    qos_app_standalone_statistics_file = dataDirName + '/' + qos_app_name + '.standalone_stats'
    with open(qos_app_standalone_statistics_file, 'w') as outfile:
        outfile.write(stats_to_print)

if __name__ == '__main__':
    if len(sys.argv) < 2:
	    print("Error: usage find_colocation_possibilities.py qos_app_name qos-policy(a number:e.g. 99, 95, 90 etc.)")
        sys.exit(1)
    find_colocation_possibilities(sys.argv[1], sys.argv[2])
