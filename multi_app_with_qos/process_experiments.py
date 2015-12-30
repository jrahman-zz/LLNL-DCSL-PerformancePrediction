#!/bin/env python

import util
import subprocess
import logging
import sys

def read_filelist(directory):
    data_points = []
    ycsb_apps = set(['mongodb', 'mysql', 'memcached', 'redis'])
    files = subprocess.check_output(['ls', directory]).decode('utf-8').split('\n')
    for f in files:
        try:
            values = f.split('.')
            data_points.append({
                'qos_app': values[0],
                'app_count': values[1],
                'filetype': values[-1],
                'file': '%(directory)s/' % locals() + f.strip(),
                'driver': 'ycsb',
                'rep': values[-2],
                'apps': '.'.join(sorted(values[2:-2])),
                'driver': 'ycsb'
            })
            if data_points[-1]['qos_app'] not in ycsb_apps:
                data_points[-1]['driver'] = 'ab'
        except:
            pass
    return data_points

def process_experiments(filename):
    data_points = read_filelist('data')

    data = []    
    for data_point in data_points:
        if data_point['filetype'] =='driver':
            if data_point['driver'] == 'ycsb':
                metrics = util.parse_ycsb(data_point['file'])
            elif data_point['driver'] == 'ab':
                metrics = util.parse_ycsb(data_point['file'])
            for metric in metrics:
                data.append({
                        'key': data_point['qos_app'] + '-' + metric,
                        'qos_app': data_point['qos_app'],
                        'apps': data_point['apps'],
                        'metric': metric,
                        'rep': data_point['rep'],
                        'value': metrics[metric]
                })
    
    with open(filename, 'w') as f:
        # Print header row
        idxs = list(data[0].keys())
        f.write(','.join(idxs) + '\n')
        # Print rows
        for item in data:
            f.write(','.join([str(item[idx]) for idx in idxs]) + '\n')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        print('Error: process_experiments.py output_filename')
    process_experiments(sys.argv[1])
