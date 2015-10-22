#!/bin/env python

import util
import subprocess
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
    experiment_name = util.apps_to_experiment_name(experiment['apps'])
    experiment_name = 'data/' + experiment_name + '.reporter'
    reporter_output = experiment['output']

    # Process PERF output into timeseries data
    process_perf(experiment_name, reporter_output)

    mean_ipc = str(None)
    mean_bubble = str(None)
    try:
        mean_ipc = mean_timeseries(experiment_name + '.ipc')
        mean_bubble = estimate_bubble(mean_ipc)
    except subprocess.CalledProcessError as e:
        logging.exception('Error: %s' % (e.output))
    except Exception as e:
        logging.exception('Exception: %s' % (str(e)))

    median_ipc = str(None)
    median_bubble = str(None)
    try:
        median_ipc = median_timeseries(experiment_name + '.ipc')
        median_bubble = estimate_bubble(median_ipc)
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
    print('%(mean_ipc)s %(mean_bubble)s %(median_ipc)s %(median_bubble)s %(rep)s %(apps)s' % locals())

def main():
    experiments = util.read_experiment_list()
    for experiment in experiments:
       process_experiment(experiment) 


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
