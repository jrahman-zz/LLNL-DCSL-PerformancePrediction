#!/bin/env python

import util
import subprocess
import multiprocessing
import sys
import logging

def process_perf(experiment_name, input_file):
    # input_file is the path to the reporter perf file
    subprocess.check_call(['../processing/process_perf.py', experiment_name, input_file])

def mean_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, 'mean']))

def median_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, 'median']))

def estimate_bubble(ipc):
    reporter_curve = '../data/reporter_curve.bubble_size.ipc.medians'
    val = subprocess.check_output(['../processing/estimate_bubble.py', reporter_curve, str(ipc)])
    return float(val)

def process_experiment(experiment):
    experiment_name = util.apps_to_experiment_name(experiment['apps'], experiment['rep'])
    logging.info('Processing %(experiment_name)s...' % locals())
    experiment_name = 'data/' + experiment_name + '.reporter'
    reporter_output = experiment['output']

    # Process PERF output into timeseries data
    process_perf(experiment_name, reporter_output)

    mean_ipc = 'NaN'
    mean_bubble = 'NaN'
    try:
        mean_ipc = mean_timeseries(experiment_name + '.ipc')
        mean_bubble = estimate_bubble(mean_ipc) / 1024.0
    except subprocess.CalledProcessError as e:
        logging.exception('Error: %s' % (e.output))
    except Exception as e:
        logging.exception('Exception: %s' % (str(e)))

    median_ipc = 'NaN'
    median_bubble = 'NaN'
    try:
        median_ipc = median_timeseries(experiment_name + '.ipc')
        median_bubble = estimate_bubble(median_ipc) / 1024.0
    except subprocess.CalledProcessError as e:
        logging.exception('Error: %s' % (e.output))
    except Exception as e:
        logging.exception('Exception: %s' % (str(e)))

    rep = experiment['rep']
    apps = []
    for app in experiment['apps']:
        apps.append(app['suite'])
        apps.append(app['bmark'])
        apps.append(app['cores'])
    apps = ' '.join(apps)
    res = '%(apps)s %(rep)s %(mean_ipc)s %(mean_bubble)s %(median_ipc)s %(median_bubble)s' % locals()
    logging.info('Processed %(experiment_name)s' % locals())
    return res

def process(experiment):
    try:
        return process_experiment(experiment)
    except Exception as e:
        logging.exception('Error: %s' % (str(e)))
        return None 

def main():
    experiments = util.read_experiment_list()
    if len(sys.argv) >= 2:
        workers = int(sys.argv[1])
    else:
        workers = 1
    pool = multiprocessing.Pool(workers)
    results = pool.map(process, experiments)
    for result in results:
        if result is not None:
            print(result)
     
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
