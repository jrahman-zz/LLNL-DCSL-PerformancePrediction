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

def create_output_path(combination, rep):
    path = 'data/' + str(len(combination)) + '_' + '.'.join([ "_".join(app) for app in combination])
    path += '.%(rep)d.reporter.perf_counters' % locals()
    return path


def main(reps, cores, maxapps):
    applications = read_applications(cores)
    for rep in range(reps):
        for app_count in range(2, maxapps + 1):
            for combination in itertools.combinations(applications, app_count):
                combo = " ".join([" ".join(app) for app in combination])
                output = create_output_path(combination, rep)

		# Subrata: lets handle one qosApp and driver combination at a time. As new applications/driver changes the way they should be handled. 
                # Hardcoding qos app name, driver name and driver workload here
		qosApp = "mongoDB"
		driverApp = "ycsb"
		driverPath= "/p/lscratche/mitra3/apps/YCSB"
		driverWorkload = driverPath + "/workloads/workloada"
                print('%(combo)s %(qosApp)s %(driverApp)s %(driverWorkload)s %(output)s %(rep)d' % locals())
#
# Parameters: create_experiments.py REPS CORES MAXAPPS
#

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Error: Invalid number of parameters")
        print("create_experiments.py REPS CORES MAXAPPS")
        sys.exit(1)
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
