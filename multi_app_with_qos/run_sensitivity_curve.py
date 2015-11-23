#!/bin/env python

import sys
import driver

MIN_CORE=0
MAX_CORE=7

DRIVER_CORES=[8,9]
QOS_CORES=[0,1]

SIZES = [256, 515, 1024, 2048, 3072, 4096, 6144, 8192, 12288, 16384, 24576, 32768, 49152, 65536]

def run_bubble(bubble_size):
    cmd = base_command(range(MAX_CORE-2,MAX_CORE))
    cmd += ['../bin/bubble', bubble_size]
    return subprocess.Popen(cmd)

def main(qos_app, driver_params):
    for size in sizes:

        output_base = '%(qos_app)s.%(size)d.%(rep)s' % locals()
        qos_data_dir = None
        bubble_proc = None
        qos_pid = None
        try:
            qos_data_dir = driver.create_qos_app_directory()
            qos_pid = driver.start_and_load_qos(qos_app, qos_data_dir, QOS_CORES, driver_params)
            driver.run_driver(output_base, qos_app, qos_pid, DRIVER_CORES, driver_params)
        finally:
            if qos_pid is not None:
                subprocess.check_call(['/bin/kill', str(qos_pid)])
                time.sleep(15) # Wait for QoS application to fully terminate
            if bubble_proc is not None:
                driver.kill_process_group(bubble_proc)
            if qos_data_dir is not None:
                driver.remove_directory(qos_data_dir)
                          
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 4:
        logging.info('Error: Invalid parameters')
        sys.exit(1)
    qos_app = sys.argv[1]
    driver_params = sys.argv[2]
    rep = int(sys.argv[3])
    
