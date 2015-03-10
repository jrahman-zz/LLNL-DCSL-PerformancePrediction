#!/usr/bin/env python

#
# Measure and record sensitivity of benchmarks to interference
# Uses PAPI instrumented versions of the benchmarks to collect
# performance counter data which is then used to characterize
# the sensitivity of the microbenchmarks to interference
#

from automation.runner.load_environ import load_environ
from automation.runner.load_interference import load_interference

from gevent.subprocess import check_output, STDOUT
import re
import json
import logging

def main():
    benchmarks = [  'dhrystone',
                'whetstone',
                'linpack',
                'stream',
                'memory_1_1024_10',
                'memory_1_1048576_10',
                'memory_1_268435456_1',
                'metadata_testing_5']
    
    reps = 40
    regex = r"PAPI - L2 Miss Rate: (\d+\.\d+)\nPAPI - L3 Miss Rate: (\d+\.\d+)\nPAPI - IPS: (\d+)"

    signatures = {}
    for benchmark in benchmarks:
        signatures[benchmark] = []

    modules = ['interference.json']
    environ = load_environ('config.json', modules)
    threads = load_interference(environ)

    #for core in [2, 1, 0]:
    #    thread = threads['StreamAdd'](environ, [core])
    #    with thread:
    #        with thread.interfere():
    #            for rep in range(0, reps):
    for rep in range(0, reps):
        for benchmark in benchmarks:
            cmd = benchmark.split('_')
            cmd[0] = '%s/%s' % (environ['benchmark_dir'], cmd[0])
            cmd = ['taskset', '-c', '0'] + cmd
            output = check_output(cmd, stderr=STDOUT)
            result = re.search(regex, output)
            if result is None:
                logging.warning('Mismatch: %s', output)
                raise Exception('No match')
            t = [-1, float(result.group(1)), float(result.group(2)), float(result.group(3))]
            signatures[benchmark].append(t)

    print "benchmark,core,l2m,l3m,ips"
    for benchmark in benchmarks:
        for sig in signatures[benchmark]:
            print "%s,%s,%s,%s,%s" % (benchmark, sig[0], sig[1], sig[2], sig[3])

if __name__ == "__main__":
    logging.basicConfig()
    main()
