#!/bin/env python

import numpy as np

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

import logging
import subprocess
import sys
import multiprocessing

suites = ['spec_fp', 'spec_int', 'parsec']

def read_data(filename):
    lines = 0
    with open(filename, 'r') as f:
        for line in f:
            lines += 1
    times = np.zeros(lines)
    ipc = np.zeros(lines)
    with open(filename, 'r') as f:
        idx = 0
        for line in f:
            values = line.strip().split()
            times[idx] = float(values[0])
            ipc[idx] = float(values[1])
            idx += 1
    return times, ipc

def get_apps(suites):
    apps = []
    for suite in suites:
        with open('manifests/%(suite)s_benchmarks' % locals(), 'r') as f:
            for line in f:
                apps.append((suite, line.strip()))
    return apps

def estimate_bubble(filename, ipc):
    try:
        return float(subprocess.check_output('${HOME}/py27/bin/python ../processing/estimate_bubble.py %(filename)s %(ipc)f 2> /dev/null' % locals(), shell=True)) / 1024.0
    except:
        return float('nan')

def func(bmark):
    
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 26}
    matplotlib.rc('font', **font)
    sns.set_palette('colorblind')

    suite, app = bmark
    reporter_curve = '../data/reporter_curve.bubble_size.ipc.medians'
    filename = 'data/%(suite)s.%(app)s.1.reporter.ipc' % locals()
    logging.info('Processing %s', filename)
    try:
        times, ipc = read_data(filename)
        times = times - np.min(times) # Normalize to 0
    except:
        return
    bubble_sizes = []
    bubbles = np.zeros(len(times))
    for i in range(len(times)):
        #if i % 50 == 0:
        #    logging.info('Estimated %d of %d bubbles', i, len(times))
        bubble_size = estimate_bubble(reporter_curve, ipc[i])
        bubbles[i] = bubble_size
        if bubble_size == bubble_size: # NaN check
            bubble_sizes.append(bubble_size)
    bubble_sizes = np.array(bubble_sizes)
    
    try:
        p99 = np.percentile(bubble_sizes, 99) * np.ones(len(times))
        p95 = np.percentile(bubble_sizes, 95) * np.ones(len(times))
        median = np.median(bubble_sizes) * np.ones(len(times))
        mean = np.mean(bubble_sizes) * np.ones(len(times))
    except:
        return
    mark_dist = int(float(len(times)) / float(20)) + 1
    plt.plot(times, bubbles, '-', times, p99, '^-', times, p95, 'o-', times, mean, 'v-', times, median, '*-', markevery=mark_dist)
    plt.xlabel('Time (s)', fontsize=18)
    plt.ylabel('Contention Score (Bubble Size [KB])', fontsize=18)
    plt.legend(['Bubble Sizes', 'p99', 'p95', 'mean', 'median'], fontsize=18)
    plt.tight_layout()
    plt.savefig('plots/%(suite)s.%(app)s.bubble_size.png' % locals(), bbox_inches='tight')
    plt.close('all')
    
    plt.plot(times, ipc, '-', markevery=mark_dist)
    plt.xlabel('Time (s)', fontsize=18)
    plt.ylabel('IPC', fontsize=18)
    plt.legend(['IPC'], fontsize=18)
    plt.tight_layout()
    plt.savefig('plots/%(suite)s.%(app)s.ipc.png' % locals(), bbox_inches='tight')
    plt.close('all')

def main(workers):
    
    apps = get_apps(suites) 
    pool = multiprocessing.Pool(workers)
    pool.map(func, apps)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(int(sys.argv[1]))
