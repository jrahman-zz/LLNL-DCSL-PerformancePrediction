#!/bin/env python

import subprocess
import logging
import time

def kill_process_group(proc):
    if proc.poll() is None:
        pid = proc.pid
        pgroup = int(subprocess.check_output('ps -o pgid= %(pid)s' % locals(), shell=True).decode('utf-8').strip())
        logging.info('Killing process group: %(pgroup)s' % locals())
        subprocess.check_call('kill -9 -%(pgroup)s' % locals(), shell=True)

def base_command(cores):
    return ['setsid', 'taskset', '-c', ','.join(map(lambda s: str(s), cores))]

def run_driver(output_base, qos_app, qos_pid, driver_cores, driver_params):
    """
    Run performance driver to determine the performance of the QoS application
    """
    logging.info('Starting QoS driver...')
  
    perf_output_path = '%(output_base)s.perf' % locals()
    driver_output_path = '%(output_base)s.driver' % locals()
 
    cmd = '../bin/time 2> "%(perf_output_path)s" ' % locals()
    cmd += '| 3>>"%(perf_output_path)s" ' % locals()
    cmd += '/usr/bin/perf stat -I 1000 -D 4000 -e cycles,instructions --append --log-fd=3 -x " " '
    cmd += '-p %(qos_pid)s ' % locals()  # subrata start collecting data on the existing pid of the qos app.i
    perf_cmd = ['setsid', 'sh', '-c', cmd]
    logging.info('Perf: ' + str(perf_cmd))

    # Context manager will control the lifetime of the process
    perf_proc = subprocess.Popen(perf_cmd)
    try:
        # jason: note in this command we are already starting to
        # monitor QoS app performance counter with 4 sec delay
        # but the driverhas not started yet

        # subrata: now start the driver (e.g. ycsb, which would drive qosApp, i.e. mongoDB .. 
        driver_cmd = base_command(driver_cores)
        driver_cmd += ['sh', 'apps/%(qos_app)s/run_driver.sh' % locals(), driver_params, driver_output_path]
        logging.info('Driver: ' + str(driver_cmd))
        # Subrata: during QoS run, we will wait till the end of the run. We have already created the benchmarks threads. After this driver run finishes we will kill all
        subprocess.check_call(driver_cmd)

        # Sanity check to ensure perf measurement is still working
        if perf_proc.poll() is not None:
            perf_proc = None
            raise Exeception('Performance counters not measured')
    finally:
        if perf_proc is not None:
            kill_process_group(perf_proc)

    # Jason: We will not return here until after the driver and performance counter
    #           monitoring processes have run to completion
    return

def start_and_load_qos(qos_app, qos_data_dir, qos_cores, driver_params):
    """
    Start a QoS application and initialize it for the experiment but loading with data etc..
    At this point, we do not want to make things unncecessarily complex by handling multiple QoS at a time
    For each QoS application, we will rather start a new experiment.
    """

    # NOTE: The start.sh script will write the PID into '%(qos_data_dir)s/app.pid'
    qoscmd = base_command(qos_cores)
    qoscmd += ['sh', 'apps/%(qos_app)s/start.sh' % locals(), qos_data_dir]

    logging.info('Starting %(qos_app)s' % locals())
    logging.info('qoscmd: %(qoscmd)s' % locals())
    qos_proc = subprocess.Popen(qoscmd)
   
    qos_pid = None
    try:
        #give time to QoS to initialize. hence sleep for 60sec
        logging.info("Waiting for QoS application to start")
        time.sleep(15)
        qos_pid = int(subprocess.check_output(['cat', '%(qos_data_dir)s/app.pid' % locals()]).decode('utf-8').strip()) 

        # Check if qos_proc as terminated, it should not have
        if qos_proc.poll() is not None:
            logging.error('QoS application terminated prematurely')
            raise Exception('QoS application terminated prematurely')

        loadcmd = ['sh', 'apps/%(qos_app)s/load.sh' % locals(), driver_params]
        logging.info('loadcmd: %(loadcmd)s' % locals())

        # Run the load script and block until finished...
        subprocess.check_call(loadcmd)
    except Exception as e:
        # In the event of a load failure, terminate the QoS app
        if qos_pid is not None:
            subprocess.check_call(['kill', '%(qos_pid)d' % locals()])
        raise # Retrow th exception so it can bubble upward

    # Sleep for 10 seconds to allow the QoS application to settle after loading
    logging.info("Sleeping for QoS to settle after loading")
    time.sleep(5)

    # Read the PID file that the 
    return qos_pid

def create_qos_app_directory():
    return subprocess.check_output(['/bin/mktemp', '--directory']).decode('utf-8').strip()

def remove_dir(directory):
    subprocess.check_call(['rm', '-rf', directory])


