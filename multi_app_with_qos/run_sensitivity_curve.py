#!/bin/env python

import sys
import driver
import logging
import subprocess
import time
import os

MIN_CORE=0
MAX_CORE=7

DRIVER_CORES=[8,9,10,11,12,13,14,15]
QOS_CORES=[0,1]

SIZES = [256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 12288, 16384, 18000, 21000, 24576, 32768, 49152, 65536]

def base_command(cores, numa_node):
    return ['setsid', 'taskset', '-c', ','.join(map(lambda s: str(s), cores)), 'numactl', '-m', str(numa_node)]

def run_bubble(bubble_size):
    cmd = base_command(range(MAX_CORE-2,MAX_CORE), 0)
    cmd += ['../bin/bubble', str(bubble_size)]
    return subprocess.Popen(cmd)

def self_pin(core):
    # Pin the python process to another socket to ensure
    # that this process doesn't interfere with the measurement
    cmd = ['taskset', '-p', '-c', str(core), str(os.getpid())]
    subprocess.check_call(cmd)

def main(qos_app, driver_params, rep):
    global SIZES
    self_pin(MAX_CORE+1)
    for size in SIZES:

        output_base = 'sensitivity_data/%(qos_app)s.%(size)d.%(rep)s' % locals()
        qos_data_dir = None
        bubble_proc = None
        qos_pid = None
        try:
            bubble_proc = run_bubble(size)
            qos_data_dir = driver.create_qos_app_directory()
            qos_proc, qos_pid = driver.start_and_load_qos(qos_app, qos_data_dir, QOS_CORES, driver_params)
            driver.run_driver(output_base, qos_app, qos_pid, DRIVER_CORES, driver_params)
        finally:
            if bubble_proc is not None:
                driver.kill_process_group(bubble_proc)
            if qos_pid is not None:
                driver.kill_process_group(qos_proc)
                time.sleep(15) # Wait for QoS application to fully terminate
            if qos_data_dir is not None:
                driver.remove_dir(qos_data_dir)
                          
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 4:
        logging.info('Error: Invalid parameters')
        sys.exit(1)
    qos_app = sys.argv[1]
    driver_params = sys.argv[2]
    rep = int(sys.argv[3])
    main(qos_app, driver_params, rep)
    
