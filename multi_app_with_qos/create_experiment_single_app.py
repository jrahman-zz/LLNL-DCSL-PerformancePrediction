#!/bin/env python

import sys

# Only 6 cores available to the application of interest
MAX_CORES=6

def read_qos_applications():
    path = 'manifest/qos'
    qos_apps = []
    with open(path, 'r') as f:
        for line in f:
            qos_apps.append(line.strip().split())
    return qos_apps

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

def create_output_path(app_count, apps, qos_app, rep):
    path = 'data/'
    path += '.'.join([qos_app, str(app_count), apps])
    path += '.%(rep)d' % locals()
    return path

def decode_apps(idx, apps, app_count, cores):
    """
    idx is the set of applications encoded as an N-ary number
    where N is the number of distinct batch applications
    """
    app_list = []
    cores_used = 0
    while app_count > 0:
        app_list.append(apps[idx % len(apps)])
        if app_list[-1][0] == 'parsec':
            cores_used += cores
        else:
            cores_used += 1
        idx = int(idx / len(apps))
        app_count -= 1
    return sorted(app_list), cores_used

def get_apps(app_count, applications, cores):
    apps = dict()
    for i in range(len(applications)**app_count):
        app_list, cores_used = decode_apps(i, applications, app_count, cores)
        if cores_used > MAX_CORES:
            continue
        key = " ".join([" ".join(app) for app in app_list])
        value =  ".".join(["_".join(app) for app in app_list]) 
        # The dictionary lets us deduplicate keys containing a sorted description
        # of the batch applications for the given co-location
        apps[key] = value
    return apps

def main(reps, cores, maxapps):
    applications = read_applications(cores)
    qos_applications = read_qos_applications()
    for qos_app, driver_workload in qos_applications:
        for rep in range(reps):
            for app_count in range(1, maxapps + 1):
                for apps, apps_dot in get_apps(app_count, applications, cores).items():
                    # Each application contains 3 space separated entries
                    # So divide by 3 to get the actual app_count
                    app_count = int(len(apps.split()) / 3)
                    output_base = create_output_path(app_count, apps_dot, qos_app, rep)
                    print('%(apps)s %(qos_app)s %(driver_workload)s %(output_base)s %(rep)d' % locals())
#
# Parameters: create_experiments.py REPS CORES MAXAPPS
#

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Error: Invalid number of parameters")
        print("create_experiments.py REPS CORES MAXAPPS")
        sys.exit(1)
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
