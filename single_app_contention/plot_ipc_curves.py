#!/bin/env python

import numpy as np

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

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
    return times, ipc

def get_apps(suites):
    apps = []
    for suite in suites:
        with open('manifest/%(suite)s_benchmarks' % locals(), 'r') as f:
            for line in f:
                apps.append((suite, line.strip()))
    return apps

def estimate_bubble(filename, ipc):
    return float(subprocess.check_output(['../processing/estimate_bubble.py', filename, ipc])) / 1024.0


def main():
    apps = get_apps(suites)
    for suite, app in apps:
        filename = 'data/%(suite)s.%(app)s.1.reporter.ipc' % locals()
        times, ipc = read_data(filename)
        times -= np.min(times) # Normalize to 0
        bubble_sizes = np.zeros(len(times))
        for i in range(len(times)):
            bubble_sizes[i] = estimate_bubble(filename, ipc[i])
        p99 = np.percentile(bubble_sizes, 99) * np.ones(len(times))
        p95 = np.percentile(bubble_sizes, 95) * np.ones(len(times))
        median = np.median(bubble_sizes) * np.ones(len(times))
        mean = np.mean(bubble_sizes) * np.ones(len(times))
        plt.plot(times, bubble_sizes, '-', times, p99, '^-', times, p95, 'o-', times, mean, 'v-', times, median, '*-')
        plt.xlabel('Time (s)')
        plt.ylabel('Contention Score (Bubble Size [KB])')
        plt.legend(['Bubble Sizes', 'p99', 'p95', 'mean', 'median'])
        plt.savefig('plots/%(suite)s.%(app)s.bubble_size.png' % locals())
        plt.close('all')
        plt.plot(times, ipc, '-')
        plt.xlabel('Time (s)')
        plt.ylabel('IPC')
        plt.legend(['IPC'])
        plt.savefig('plots/%(soutes.%(app)s.ipc.png' % locals())
        plt.close('all')

if __name__ == '__main__':
    pass
