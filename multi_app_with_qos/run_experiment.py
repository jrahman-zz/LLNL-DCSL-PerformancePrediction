#!/bin/env python

import os
import sys
import subprocess
import logging
import threading
import functools
import time

import json
import requests

import driver

def ensure_data_dir():
    # Ensure that the data directory is created
    subprocess.check_call(['mkdir', '-p', 'data'])

def self_pin(core):
    # Pin the python process to another socket to ensure
    # that this process doesn't interfere with the measurement
    cmd = ['taskset', '-p', '-c', str(core), str(os.getpid())]
    subprocess.check_call(cmd)

def base_command(cores):
    return ['setsid', 'taskset', '-c', ','.join(map(lambda s: str(s), cores))]

# 
procs = dict()
lock = threading.Lock()

def run_thread(func):
    """
    Decorator to run a function inside it's own thread
    Its assumed the function will return a Process object back
    """
    def wrapper(slot, bmark, cores):
        with lock:
            procs[slot] = None
        def run():
            global procs
            while True:
                proc = None
                with lock:
                    procs[slot] = func(bmark, cores)
                    proc = procs[slot]
                retcode = proc.wait()
                logging.info('%(bmark)s finished' % locals())
                with lock:
                    # The main experiment function will set this to None
                    # if the driver has finished, so if that is the case
                    # we should break immediately
                    if procs[slot] is None:
                        break
                    procs[slot] = None
                # retcode == 0 indicates normal termination of the batch process
                # while retcode==9 indicates that it was killed intentionally
                if retcode != 0 and retcode != -9:
                    raise Exception('Non-zero return code: %(retcode)d' % locals())
        thread = threading.Thread(target=run)
        logging.info('Starting thread for %(bmark)s' % locals())
        thread.start()
        return thread
    return wrapper

# List containing completion counts for the ith process
run_counts = []
def add_slot():
    """
    Add a new slot for another batch application
    """
    global run_counts
    run_counts.append(0)
    return len(run_counts) - 1

@run_thread
def run_spec(bmark, cores):
    cmd = base_command(cores)
    cmd += ['runspec', '--nosetprocgroup', '--nobuild', '--config', 'research_config', '--action', 'onlyrun', '--size', 'ref', bmark]
    logging.info('Starting %(bmark)s' % locals())
    return subprocess.Popen(cmd)

@run_thread
def run_parsec(bmark, cores):
    core_count = len(cores)
    cmd = base_command(cores)
    cmd += ['parsecmgmt', '-a', 'run', '-i', 'native', '-n', str(core_count), '-p', bmark]
    logging.info('Starting %(bmark)s' % locals())
    return subprocess.Popen(cmd)

# Application format is '(suite bmark cores)+ output_base rep'
def run_experiment(params, output_base, rep):
    """
    old format (suite bmark #cores)+
    new format: (suite bmark #cores)+ qos_app driver_params output_base rep
    """
    #print params
    #return

    applications = []                            # subrata need to save the benchmark results in a file. and pass the name of that file here
    for i in range(int((len(params) - 4) / 3)):  # subrata : parsing of the already created experiment list generated by "create_experiment.py"
        suite = params[3 * i]
        bmark = params[1 + 3 * i]
        cores = int(params[2 + 3 * i])
        applications.append([suite, bmark, cores])
    logging.info('Starting experiment with %d applications' % (len(applications)))
    
    driver_params = params[-3]
    qos_app = params[-4]
    #driverWorkload = params[-3]

    # Cab contains 8 cores per SMP
    #reporter_core = 0    #subrata : reporter will be replaced by mongodB (interactive) => use two cores. YCSB will be in the other socket 2 cores anything between (8-15)
    qos_cores = [0,1]    #subrata : specify the cores that qos app would use
    starting_core = 2
    ending_core = 7
    current_core = 2
    driver_cores = [8,9]
    max_core = 15
    core_allocations = []
    for application in applications:
        cores = int(application[2])
        if current_core + cores - 1 <= ending_core:
            core_allocations.append(list(range(current_core, current_core + cores)))
            current_core += cores # This is appearently important...
        else:
            # TODO, error
            pass

    logging.info('Applications: ' + str(applications))
    # Pin ourself to the other socket
    #self_pin(ending_core+1)   # subrata : self pining of "this" python driver. similarly pin the benchmark driver YCSB/ apache bench etc. Pin tghem on the other socket to reduce intf
    self_pin(max_core)   # subrata : self pining of "this" python driver. similarly pin the benchmark driver YCSB/ apache bench etc. Pin tghem on the other socket to reduce intf
   
    #subrata: based on the already generated unique output path, create a temporary data store path for qos app (in /tmp/)

    #now run and initialize the qos app...at the end of the experiment we will kill this qos app, so at this moment do not worry about the state
    qos_pid = None
    qos_data_dir = None
    try: 
        qos_data_dir = driver.create_qos_app_directory()
        qos_pid = driver.start_and_load_qos(qos_app, qos_data_dir, qos_cores, driver_params)

        ensure_data_dir()

        experiment = ".".join(['%(suite)s_%(bmark)s_%(cores)d' % locals() for suite, bmark, cores in applications])

        threads = []

        # Launch batch applications...
        for i in range(len(applications)):
            application = applications[i]
            cores = core_allocations[i]
            suite = application[0]
            bmark = application[1]
            if suite == 'parsec':
                # Notice that the parameters here reflect the def wrapper() function in the decorator
                threads.append(run_parsec(add_slot(), bmark, cores))
            elif suite == 'spec_fp' or suite == 'spec_int':
                threads.append(run_spec(add_slot(), bmark, cores))
            else:
                raise Exception('Bad suite: %(suite)s' % locals())

        logging.info('Sleeping to allow batch applictions to start...')
        time.sleep(30)
        try:
            logging.info('Starting driver')
            driver.run_driver(output_base, qos_app, qos_pid, driver_cores, driver_params) 
            logging.info('Finished running driver')
        except Exception as e:
            logging.exception("Error: Failed to start reporter")
            with lock:
                for key in procs:
                    if procs[key] is not None:
                        driver.kill_process_group(procs[key])
                        procs[key] = None
            for thread in threads:
	            thread.join()
            sys.exit(1)

        # Kill the benchmark threads as the main thread running the driver has finished
        with lock:
            for key in procs:
                if procs[key] is not None:
                    driver.kill_process_group(procs[key])
                    procs[key] = None    

        # Wait for threads to return
        for thread in threads:
            thread.join()
    
    except Exception as e:
        logging.exception('Problem while running experiment' + str(e))
    finally:
        #subrata: now kill the qos app as well. We will relaunch it during next experiment run

        if qos_pid is not None:
            subprocess.check_call(['/bin/kill', str(qos_pid)])
            time.sleep(10) # Wait for QoS app to fully terminate

        #subrata: now since this experiment has completed, remove the directory used for data store
        if qos_data_dir is not None:
            driver.remove_dir(qos_data_dir)


def send_request(host, port, endpoint, method='GET', body=None):
    url = 'http://%(host)s:%(port)d/%(endpoint)s' % locals()
    logging.info('Sending to url "%(url)s"' % locals())
    if method == 'GET':
        return requests.get(url).text
    else:
        return requests.post(url, data=body).text

def get_experiment(host, port):
    return send_request(host, port, 'get_experiment')    

def send_success(host, port, experiment):
    body = {'experiment': experiment, 'success': True}
    send_request(host, port, 'return_experiment', 'POST', json.dumps(body))

def send_failure(host, port, experiment, message):
    body = {'experiment': experiment, 'success': False, 'message': message}
    send_request(host, port, 'return_experiment', 'POST', json.dumps(body))

def run_slave(host, port):
    # Run as a slave worker on a node
    keep_running = True
    while keep_running:
        keep_running = False
        logging.info('Getting experiment...')
        experiment = get_experiment(host, port)
        try:
            parsed_experiment = experiment.split()
            size = len(parsed_experiment)
            logging.info('Retrieved experiment: %(experiment)s with %(size)d entries' % locals())
            run_experiment(parsed_experiment, parsed_experiment[-2], int(parsed_experiment[-1]))
            send_success(host, port, experiment)
            keep_running = True
        except Exception as e:
            logging.info('Failed experiment: %(experiment)s' % locals())
            logging.exception('Error: %s' % str(e))
            send_failure(host, port, experiment, str(e))

if __name__ == '__main__':
   
    logging.basicConfig(level=logging.DEBUG)
     
    # Two parameters for the rep and the name of the program
    # All others are 3*i where i is the number of batch applications
    if len(sys.argv) == 3:
        # Host and port of the master...
       run_slave(sys.argv[1], int(sys.argv[2]))
    elif (len(sys.argv) - 5) % 3 == 0:
        # Parameters given on the command line
        run_experiment(sys.argv[1:], sys.argv[-2], int(sys.argv[-1]))
    else:
        print('Error: Invalid parameters')
