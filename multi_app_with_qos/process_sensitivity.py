#!/usr/apps/python3.4.2/bin/python3

import numpy as np
import pandas as pd

import pickle
import sys
import subprocess
import logging

import util
from sklearn.isotonic import IsotonicRegression

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

def process_perf(experiment_name, input_file):
    subprocess.check_call(['../processing/process_perf.py', experiment_name, input_file])

def mean_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, 'mean']).decode('utf-8').strip())

def median_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, 'median']).decode('utf-8').strip())

def get_mean_ipc(path):
    process_perf('tmp_exp', path)
    return mean_timeseries('tmp_exp.ipc')

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
        x = group['bubble_size_kb']
        y = group['value']
        start = y[y.idxmin()]
        end = y[y.idxmax()]
        if start < end:
            increasing = True
        else:
            increasing = False
        curve = IsotonicRegression(increasing=increasing)
        curve.fit(x, y)
        curves[qos_app][metric] = curve

    with open(filename, 'w') as f:
        pickle.dump(curves, f, pickle.HIGHEST_PROTOCOL)
    return curves
    
def plot_curves(data, curves):
    for level, group in data.groupby('key'):
        d = group.sort('bubble_size_kb')
        sns.pointplot(data=d, estimator=np.median, y='value', x='bubble_size_kb', join=True)
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=45)
        plt.ylabel(level)
        plt.xlabel('Bubble Size (KB)')
        plt.legend()
        plt.savefig(level + '.png')
        plt.close()

def process_sensitivity(filename):
    data_points = read_filelist('sensitivity_data')
    data = {'key': [], 'qos_app': [], 'bubble_size_kb': [], 'metric': [], 'rep': [], 'value': []}
    for data_point in data_points:
        if data_point['type'] == 'driver':
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
            continue
            mean_ipc = get_mean_ipc(data_point['file'])
            data['key'].append(data_point['qos_app'] + "-IPC")
            data['qos_app'].append(data_point['qos_app'])
            data['bubble_size_kb'].append(data_point['bubble_size'])
            data['metric'].append('IPC')
            data['rep'].append(data_point['rep'])
            data['value'].append(mean_ipc)
 
    data = pd.DataFrame(data)
    
    curves = build_curves(data, filename)
    plot_curves(data, curves)
 
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: usage process_sensitivity.py OUTPUT_FILENAME")
        sys.exit(1)
    process_sensitivity(sys.argv[1])
