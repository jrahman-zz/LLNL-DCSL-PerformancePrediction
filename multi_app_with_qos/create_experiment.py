#!/bin/env python

import itertools
import sys

def read_applications(cores):
    suites = ['spec_fp', 'spec_int', 'parsec']
    applications = []
    for suite in suites:
        path = 'manifest/%(suite)s' % locals()
        if suite == 'parsec':
            app_cores = cores
        else:
            app_cores = 1
        with open(path, 'r') as f:
            for line in f:
                applications.append([suite, line.strip(), str(app_cores)])
    return applications

def create_output_path(combination, qos_app, rep):
    app_str = '.'.join(['_'.join(app) for app in combination])
    path = 'data/'
    path += '_'.join([qos_app, str(len(combination)), app_str])
    path += '.%(rep)d' % locals()
    return path

def main(reps, cores, maxapps):
    applications = read_applications(cores)
    qos_app = "mongodb"
    driver_workload = "workloada"

    for rep in range(reps):
        for app_count in range(2, maxapps + 1):
            for combination in itertools.combinations(applications, app_count):
                combo = " ".join([" ".join(app) for app in combination])
                output_base = create_output_path(combination, qos_app, rep)

		# Subrata: lets handle one qosApp and driver combination at a time. As new applications/driver changes the way they should be handled. 
                print('%(combo)s %(qos_app)s %(driver_workload)s %(output_base)s %(rep)d' % locals())
#
# Parameters: create_experiments.py REPS CORES MAXAPPS
#

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Error: Invalid number of parameters")
        print("create_experiments.py REPS CORES MAXAPPS")
        sys.exit(1)
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
