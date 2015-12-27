#!/usr/apps/python3.4.2/bin/python3

import numpy as np
import pandas as pd

import sys
import subprocess
import logging

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

def parse_ab(path):

    results = dict()

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            prefix = line[0:3]
            if prefix == '95%':
                value = int(line.split()[1])
                results['READ.95thPercentileLatency(us)'] = value * 1000
            elif prefix == '99%':
                value = int(line.split()[1])
                results['READ.99thPercentileLatency(us)'] = value * 1000
            else:
                prefix = line[0:6]
                if prefix == 'Total:':
                    value = float(line.split()[2])
                    results['READ.AverageLatency(us)'] = value * 1000
                elif prefix == 'Reques':
                    value = float(line.split()[3]) * 1000
                    results['OVERALL.Throughput(ops_per_sec)'] = value * 1000
    return results

def parse_ycsb(path):
    metrics = set([
                'AverageLatency(us)',
                '95thPercentileLatency(us)',
                '99thPercentileLatency(us)'
                ])
    categories = set(['[READ]', '[UPDATE]'])
    total_runtime = 0
    results = dict()
    with open(path, 'r') as f:
        for line in f:
            data = line.strip().split(', ')
            if data[0] == '[OVERALL]' and data[1] == 'Throughput(ops/sec)':
                results[data[0][1:-1] + ".Throughput(ops_per_sec)"] = float(data[2])
            if data[0] in categories and data[1] in metrics:
                results[data[0][1:-1] + "." + data[1]] = float(data[2]) 
    return results

def read_filelist():
    data_points = []
    directory = 'sensitivity_data'
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
        except Exception as e:
            pass
    return data_points

def process_sensitivity(filename):
    data_points = read_filelist()
    data = {'key': [], 'qos_app': [], 'bubble_size_kb': [], 'metric': [], 'rep': [], 'value': []}
    for data_point in data_points:
        if data_point['type'] == 'driver':
            if data_point['driver'] == 'ycsb':
                metrics = parse_ycsb(data_point['file'])
                for metric in metrics:
                    data['key'].append(data_point['qos_app'] + "-" + metric)
                    data['qos_app'].append(data_point['qos_app'])
                    data['bubble_size_kb'].append(data_point['bubble_size'])
                    data['metric'].append(metric)
                    data['rep'].append(data_point['rep'])
                    data['value'].append(metrics[metric])
        elif data_point['type'] == 'perf':
            mean_ipc = get_mean_ipc(data_point['file'])
            data['key'].append(data_point['qos_app'] + "-IPC")
            data['qos_app'].append(data_point['qos_app'])
            data['bubble_size_kb'].append(data_point['bubble_size'])
            data['metric'].append('IPC')
            data['rep'].append(data_point['rep'])
            data['value'].append(mean_ipc)
 
    data = pd.DataFrame(data)
    with open(filename, 'w') as f:
        data.to_csv(path_or_buf=f, sep=',', header=True)
    
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

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: usage process_sensitivity.py OUTPUT_FILENAME")
        sys.exit(1)
    process_sensitivity(sys.argv[1])
