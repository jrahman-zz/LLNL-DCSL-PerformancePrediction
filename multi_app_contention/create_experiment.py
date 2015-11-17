#!/bin/env python

#import itertools
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

def create_output_path(app_count, apps, rep):
    path = 'data/' + str(app_count) + apps
    path += '.%(rep)d.reporter.perf_counters' % locals()
    return path

def decode_apps(idx, apps, app_count):
    app_list = []
    while app_count > 0:
        app_list.append(apps[idx % len(apps)])
        idx = int(idx / len(apps))
        app_count -= 1
    return sorted(app_list)

def get_apps(app_count, applications):
    apps = dict()
    for i in range(len(applications)**app_count):
        app_list = decode_apps(i, applications, app_count)
        key = " ".join([" ".join(app) for app in app_list])
        value =  ".".join(["_".join(app) for app in app_list]) 
        apps[key] = value
    return apps

def main(reps, cores, maxapps):
    applications = read_applications(cores)
    for rep in range(reps):
        for app_count in range(2, maxapps + 1):
            for apps, apps_dot in get_apps(app_count, applications).items():
                output = create_output_path(app_count, apps_dot, rep)
                print('%(apps)s %(output)s %(rep)d' % locals())
#
# Parameters: create_experiments.py REPS CORES MAXAPPS
#

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Error: Invalid number of parameters")
        print("create_experiments.py REPS CORES MAXAPPS")
        sys.exit(1)
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
