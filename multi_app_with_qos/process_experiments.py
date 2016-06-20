#!/bin/env python

import util
import subprocess
import multiprocessing
import sys
import logging

#qos_name = 'reporter'  #Actually it will be the name of the qos app

def process_perf(experiment_name, input_file):
    # input_file is the path to the reporter perf file
    subprocess.check_call(['../processing/process_perf.py', experiment_name, input_file])

def mean_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, 'mean']))

def median_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, 'median']))

def p99_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, '99th']))

def p95_timeseries(path):
    return float(subprocess.check_output(['../processing/average_timeseries.py', path, '95th']))

def estimate_bubble(ipc, qos_name):
    reporter_curve = '../data/reporter_curve.bubble_size.ipc'
    # subrata: we should use the following qos specific curve instead
    #reporter_curve = '../data/' + qos_name + '_curve.bubble_size.ipc'
    val = subprocess.check_output(['../processing/estimate_bubble.py', reporter_curve, str(ipc)])
    return float(val)

def process_experiment(experiment):
    qos_name = experiment['qos_name']
    experiment_name = qos_name + '.' + util.apps_to_experiment_name(experiment['apps'], experiment['rep'])
    logging.info('Processing %(experiment_name)s...' % locals())
    experiment_name = 'data/' + experiment_name
    reporter_output = experiment['output'] + '.perf'

    # Process PERF output into timeseries data
    process_perf(experiment_name, reporter_output)

    mean_ipc = 'NaN'
    mean_bubble = 'NaN'
    try:
        mean_ipc = mean_timeseries(experiment_name + '.ipc')
        mean_bubble = estimate_bubble(mean_ipc, qos_name) / 1024.0
    except subprocess.CalledProcessError as e:
        logging.exception('Error: %s' % (e.output))
    except Exception as e:
        logging.exception('Exception: %s' % (str(e)))

    median_ipc = 'NaN'
    median_bubble = 'NaN'
    try:
        median_ipc = median_timeseries(experiment_name + '.ipc')
        median_bubble = estimate_bubble(median_ipc, qos_name) / 1024.0
    except subprocess.CalledProcessError as e:
        logging.exception('Error: %s' % (e.output))
    except Exception as e:
        logging.exception('Exception: %s' % (str(e)))

    p95_ipc = 'NaN'
    p95_bubble = 'NaN'
    try:
        p95_ipc = p95_timeseries(experiment_name + '.ipc')
        p95_bubble = estimate_bubble(p95_ipc, qos_name) / 1024.0
    except subprocess.CalledProcessError as e:
        logging.exception('Error: %s' % (e.output))
    except Exception as e:
        logging.exception('Exception: %s' % (str(e)))
   
    p99_ipc = 'NaN'
    p99_bubble = 'NaN'
    try:
        p99_ipc = p99_timeseries(experiment_name + '.ipc')
        p99_bubble = estimate_bubble(p99_ipc, qos_name) / 1024.0
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
    res = '%(apps)s %(rep)s %(mean_ipc)s %(mean_bubble)s %(median_ipc)s %(median_bubble)s %(p95_ipc)s %(p95_bubble)s %(p99_ipc)s %(p99_bubble)s' % locals()
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
    #for e in experiments:
    #	    print e
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
