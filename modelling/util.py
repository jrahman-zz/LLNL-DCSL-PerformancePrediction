#!/bin/env python

import pandas as pd
import numpy as np

def read_manifest():
    apps = []
    suites = ['parsec', 'spec_fp', 'spec_int']
    for suite in suites:
        with open('manifest/%(suite)s' % locals(), 'r') as f:
            for line in f:
                apps.append({'suite': suite, 'bmark': line.strip()}) 
    return apps  

def parse_row(row):
    parsed = dict()
    parsed['mean_ipc'] = float(row[-4])
    parsed['median_ipc'] = float(row[-2])
    parsed['mean_bubble'] = float(row[-3])
    parsed['median_bubble'] = float(row[-1])
    rep = row[-5]
    parsed['rep'] = int(rep)
    apps = row[0:-5]
    app_list = []
    for i in range(int(len(apps) / 3)):
        suite = apps[3*i]
        bmark = apps[3*i + 1]
        
        if suite not in parsed:
            parsed[suite] = 0
        parsed[suite] += 1
        
        app = '_'.join([suite, bmark])
        if app not in parsed:
            parsed[app] = 0
        parsed[app] += 1

        app_list.append(app)

    parsed['apps'] = '.'.join(app_list)
    parsed['app_count'] = len(apps) / 3
    return parsed

def read_data(filename):
    """ Format is
        '(suite bmark cores)+ rep mean_ipc mean_bubble median_ipc median_bubble' 
    """

    data = dict()
   
    # Read the line count ahead of time...
    lines = 0
    with open(filename, 'r') as f:
        for line in f:
            lines += 1

    apps = read_manifest()

    # Build empty dict will all required keys...
    app_count = 0

    data['apps'] = ['' for i in range(lines)]
    data['app_count'] = np.zeros(lines)
    data['mean_ipc'] = np.zeros(lines)
    data['median_ipc'] = np.zeros(lines)
    data['mean_bubble'] = np.zeros(lines)
    data['median_bubble'] = np.zeros(lines)
    data['rep'] = ['' for i in range(lines)]

    # Populate application counts
    apps = read_manifest()
    for app in apps:
        data[app['suite'] + '_' + app['bmark']] = [0 for i in range(lines)]
    for suite in set([item['suite'] for item in apps]):
        data[suite] = [0 for i in range(lines)]

    with open(filename, 'r') as f:
        idx = 0
        for line in f:
            row = parse_row(line.strip().split())
            for key, value in row.items():
                data[key][idx] = value
            idx += 1

    dataframe = pd.DataFrame()
    for key, value in data.items():
        dataframe[key] = value
    return dataframe

if __name__ == '__main__':
    pass
