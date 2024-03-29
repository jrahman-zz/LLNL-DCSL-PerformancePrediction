#!/bin/env python

import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import numpy as np

import random
import itertools
import sys
import json
import requests
import logging

data_file = 'als_data'

def parse_experiment(exp):
    """
    Format: 'appcount:fraction,appcount:fraction,...,appcount:fraction rank rep'
    Note that we define a different fraction per appcount
    so we can vary the density for each section of the matrix
    """
    parsed_experiment = dict()
    parsed_experiment['fractions'] = {int(pair.split(':')[0]): float(pair.split(':')[1]) for pair in exp.split()[0].split(',')}
    parsed_experiment['rank'] = int(exp.split()[1])
    parsed_experiment['rep'] = int(exp.split()[2])
    return parsed_experiment

def create_training(apps, data, fraction, app_count):
    training_data = []

    # For each column, track the apps (row) that have been filled
    columns = dict()
    total_entries = 0
    filled_entries = 0

    combinations = [sorted(c) for c in itertools.combinations(apps, app_count - 1)]
    for combination in combinations:
        total_entries += len(apps)
        columns['.'.join(sorted(combination))] = set()
    logging.info('Total entries: %(total_entries)d' % locals())
    
    # The app_count-1 sized subsets represent the column keys
    for combination in combinations:
        # Try to fill in at least one entry per column first
        column_key = '.'.join(sorted(combination))
        filled_fraction = float(filled_entries) / float(total_entries)
        print(filled_fraction, fraction)
        if len(columns[column_key]) == 0 and filled_fraction < fraction:
            # Pick a random row (app) within the column
            choice = random.choice(apps)
            while choice in columns[column_key]:
                choice = random.choice(apps)
            entry_apps = sorted([choice] + combination)
            # For A.B.C Look at the different combinations such as [A, B.C], [B, A.C], etc
            for i in range(len(entry_apps)):
                first_app = entry_apps[i]
                remaining_apps = '.'.join(entry_apps[0:i] + entry_apps[i+1:])
                entry_key = '.'.join(entry_apps)
                if remaining_apps in columns and first_app not in columns[remaining_apps] and entry_key in data:
                        
                    print(entry_key, remaining_apps)
                    filled_entries += 1
                    # Record that the row with first app has been filled in the column
                    columns[remaining_apps].add(first_app)
                    training_data.append((first_app, remaining_apps, data[entry_key]))
        
    # Now that we've filled at least one entry per column
    # fill in extra until we hit the target fraction
    all_keys = [sorted(c) for c in itertools.combinations(apps, app_count)]
    random.shuffle(all_keys)
    idx = 0
    while idx < len(all_keys) and float(filled_entries) / float(total_entries) < fraction:
        entry_apps = all_keys[idx]
        idx += 1
        entry_key = '.'.join(entry_apps)
        if entry_key not in data:
            print('Entry: %(entry_key)s not in data' % locals())
            continue
        for i in range(len(entry_apps)):
            first_app = entry_apps[i]
            remaining_apps = '.'.join(entry_apps[0:i] + entry_apps[i+1:])
            if first_app not in columns[remaining_apps]:
                filled_entries += 1
                columns[remaining_apps].add(first_app)
                training_data.append((first_app, remaining_apps, data[entry_key]))
    # Check the number of columns with no entry...
    empty_columns = set()
    for key, value in columns.items():
        if len(value) == 0:
            print('Column: %(key)s is empty' % locals())
            empty_columns.add(key)
    print('There are %d empty_columns' % (len(empty_columns)))
    return training_data, empty_columns

def build_training(apps, data, fractions, maxapps):
    training_data = []
    empty_columns = []
    for app_count in range(2, maxapps+1):
        logging.info('Creating training data for %(app_count)d apps' % locals())
        data_points, columns = create_training(apps, data, fractions[app_count], app_count)
        for data_point in data_points:
            training_data.append(data_point)
        for column in columns:
            empty_columns.append(column)
    return training_data, empty_columns
   
def load_bubbles():
    bubbles = dict()
    with open(data_file, 'r') as f:
        for line in f:
            values = line.strip().split()
            bubbles[values[0]] = float(values[1])
    return bubbles

def load_mappings():
    # The ALS implementation uses numeric labels for items
    # So we need to maintain a consistent set of mappings from applications and
    # application combinations into numeric labels used by the ALS algorithm
    ylabels = {line.strip().split(',')[0]: int(line.strip().split(',')[1]) for line in open('ylabels')}
    xlabels = {line.strip().split(',')[0]: int(line.strip().split(',')[1]) for line in open('xlabels')}
    ymapping = [line.strip().split(',')[0] for line in open('ylabels')]
    xmapping = [line.strip().split(',')[0] for line in open('xlabels')]
    return ylabels, xlabels, ymapping, xmapping 

def process_value(x):
    apps = x[0].split('.')
    output = []
    for i in range(len(apps)):
        first_app = apps[i]
        remaining_apps = '.'.join(apps[0:i] + apps[i+1:])
        output.append((first_app, remaining_apps, x[1]))
    return output

def run_experiment(fractions, rank, rep):
    conf = (pyspark.SparkConf()
                .setMaster('local')
                .setAppName('PerformancePredictionALS')
                .set('spark.executor.memory', '2g'))
    sc = SparkContext(conf = conf)
  
    print(fractions)
     
    ylabels, xlabels, ymapping, xmapping = load_mappings()       

    # Load bubble data for single and multiple applications
    bubble_data = load_bubbles()
    maxapps = max([len(apps.split('.')) for apps in bubble_data.keys()])
    apps = [app for app in bubble_data.keys() if len(app.split('.')) == 1]

    train_data, empty_columns = build_training(apps, bubble_data, fractions, maxapps)
    training = sc.parallelize(train_data)
    # Apply mappings from application names, to numeric IDs
    training = training.map(lambda x: Rating(ylabels[x[0]], xlabels[x[1]], x[2]))
    model = ALS.train(training, rank, 10)

    # Create Rating objects for the entire dataset
    test = sc.parallelize([(key, value) for key, value in bubble_data.items()])
    test = test.flatMap(process_value)
    test = test.map(lambda x: Rating(ylabels[x[0]], xlabels[x[1]], x[2]))

    predictions = model.predictAll(test.map(lambda x: (x[0], x[1]))).map(lambda x: ((x[0], x[1]), x[2]))
    bubble_sizes = test.map(lambda x: ((x[0], x[1]), x[2]))
    
    # Both predictions and rating have the form of [(K, V1), ...], [(K, V2), ...] so join both up
    # to the form of [(K, [V1, V2]), ...]
    test_predictions = test.join(predictions)
    
    # Convert back to (yapp, xapps, error) tuples
    # x[0] is a tuple with the y and x axis numeric labels x[1] is a (predicted, observed) tuple
    test_predictions = test_predictions.map(lambda x: (ymapping[x[0][0]], xmapping[x[0][1]], (x[1][0] - x[1][1])/x[1][1]))
    # test_predictions tuples contain (yappname, xappnames, percent_error, observed_bubble)
    errors = test_predictions.map(lambda x: ('.'.join(sorted([x[0]] + x[1].split('.'))), x[0], x[1], x[2])).collect()
    
    print('apps yapp xapps rel_error observed rank fraction rep')
    for apps, yapp, xapps, error, observed in errors:
        fraction = fractions[len(apps.split('.'))]
        observed = bubble_sizes[apps]
        print('%(apps)s %(yapp)s %(xapps)s %(error)f %(observed)f %(rank)d %(fraction)f %(rep)f' % locals())

def send_request(host, port, endpoint, method='GET', body=None):
    url = 'http://%(host)s:%(port)d/%(endpoint)s' % locals()
    logging.info('Sending to url "%(url)s"' % locals())
    if method == 'GET':
        return requests.get(url).text
    else:
        return requests.post(url, data=body).text

def get_experiment(host, port):
    return send_request(host, port, 'get_experiment')

def send_success(host, port, experiment):
    body = {'experiment': experiment, 'success': True}
    send_request(host, port, 'return_experiment', 'POST', json.dumps(body))

def send_failure(host, port, experiment, message):
    body = {'experiment': experiment, 'success': True}
    send_request(host, port, 'return_experiment', 'POST', json.dumps(body))

def run_slave(host, port):
    keep_running = True
    while keep_running:
        keep_running = False
        logging.info('Getting experiment...')
        experiment = get_experiment(host, port)
        try:
            parsed_experiment = parse_experiment(experiment.strip())
            fractions = parsed_experiment['fractions']
            rank = parsed_experiment['rank']
            rep = parsed_experiment['rep']
            run_experiment(fractions, rank, rep)
            keep_running = True
        except Exception as e:
            logging.info('Failed experiment: %(experiment)s' % locals())
            logging.exception('Error: %s' % str(e))
            send_failure(host, port, experiment, str(e))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) == 3:
        run_slave(sys.argv[1], int(sys.argv[2]))
    else:
        parsed_experiment = parse_experiment(' '.join(sys.argv[1:]))
        fractions = parsed_experiment['fractions']
        rank = parsed_experiment['rank']
        rep = parsed_experiment['rep']
        run_experiment(fractions, rank, rep)
