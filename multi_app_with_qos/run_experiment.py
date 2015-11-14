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

YCSB_DIR="/p/lscratche/mitra3/apps/YCSB/"

def ensure_data_dir():
    # Ensure that the data directory is created
    subprocess.check_call(['mkdir', '-p', 'data'])

def self_pin(core):
    # Pin the python process to another socket to ensure
    # that this process doesn't interfere with the measurement
    cmd = ['taskset', '-p', '-c', str(core), str(os.getpid())]
    subprocess.check_call(cmd)

def base_command(cores):
    return ['taskset', '-c', ','.join(map(lambda s: str(s), cores))]

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
                #if update_count(slot) == False:
                    # Finished running, kill all other running procs since
                    # update_count() has indicated that each process has
                    # fully run at least one time
                #    with lock:
                #        logging.info('Killing extra procs')
                #        for key in procs:
                #            if procs[key] is not None:
                #                try:
                #                    procs[key].kill()
                #                except Exception as e:
                #                    logging.exception("Failed to kill proc")
        thread = threading.Thread(target=run)
        logging.info('Starting thread for %(bmark)s' % locals())
        thread.start()
        return thread
    return wrapper

@run_thread
def run_spec(bmark, cores):
    cmd = base_command(cores)
    cmd += ['runspec', '--nobuild', '--config', 'research_config', '--action', 'onlyrun', '--size', 'ref', bmark]
    logging.info('Starting %(bmark)s' % locals())
    return subprocess.Popen(cmd)

@run_thread
def run_parsec(bmark, cores):
    core_count = len(cores)
    cmd = base_command(cores)
    cmd += ['parsecmgmt', '-a', 'run', '-i', 'native', '-n', str(core_count), '-p', bmark]
    logging.info('Starting %(bmark)s' % locals())
    return subprocess.Popen(cmd)

def getQoSWithDriverCommand(qosAppName, driverAppName, driverWorkload, driverResultsPath):
    driverRunCommand = ""
    #driverRunCommand += YCSB_DIR + "ycsb run mongodb -s -P " + driverWorkload + " | tee " + driverResultsPath
    currentDir = "/g/g90/mitra3/scheduling_work/LLNL-DCSL-PerformancePrediction/multi_app_with_qos/"
    driverRunCommand += currentDir + "mongoDB_by_ycsb.sh run " + driverWorkload + " | tee " + driverResultsPath
    return driverRunCommand

def run_driver(output_path, pid_file, qosAppName, qos_pid, driverAppName, driver_cores, driverWorkload, driverResultsPath):
    logging.info('Starting QoS appr...')
    
    #cores = ",".join(map(lambda s: str(s), cores))
    driver_cores = ",".join(map(lambda s: str(s), driver_cores))

    cmd = '../bin/time 2> "%(output_path)s" ' % locals()
    cmd += '| 3>>"%(output_path)s" taskset -c %(driver_cores)s ' % locals()  # subrata cores => comma seperated list of cores
    cmd += '/usr/bin/perf stat -I 1000 -D 15000 -e cycles,instructions --append --log-fd=3 -x " " '
    cmd += '-p %(qos_pid)s ' % locals()  # subrata start collecting data on the existing pid of the qos app.
    cmd += '1> %(pid_file)s' % locals() #subrata : we will first start collecting data and then start the driver in the next few lines. Will the locking mechanism create problem ?
    logging.info(cmd)  
    subprocess.Popen(cmd, shell=True) # subrata: note in this command we are already starting to monitor QoS app with 15 sec delay..but the driverhas not started yet

    # subrata: now start the driver (e.g. ycsb, which would drive qosApp, i.e. mongoDB .. 
    driver_run_cmd = getQoSWithDriverCommand(qosAppName, driverAppName, driverWorkload, driverResultsPath) # subrata: this command will drive the QoS app
    logging.info(driver_run_cmd)
    # Subrata: during QoS run, we will wait till the end of the run. We have already created the benchmarks threads. After this driver run finishes we will kill all
    subprocess.check_call(driver_run_cmd, shell=True)

# List containing completion counts for the ith process
run_counts = []

def update_count(slot):
    """
    Update the counts for a given process and determine if all processes
    finished at least once, in which case we actually return false
    """
    global run_counts
    global lock
    with lock:
        run_counts[slot] += 1
        return functools.reduce(lambda x, y: x*y, run_counts, 1) == 0

def add_slot():
    """
    Add a new slot for another batch application
    """
    global run_counts
    run_counts.append(0)
    return len(run_counts) - 1

def run_and_initialize_qos(qosAppName, qosAppDataPath, driverName, qos_cores, driverWorkload):
    """
    Start a QoS application and initialize it for the experiment but loading with data etc..
    At this point, we do not want to make things unncecessarily complex by handling multiple QoS at a time
    For each QoS, we will rather start a new experiment."""
    qoscmd = base_command(qos_cores)
    qoscmd += ['mongod' , '--dbpath', qosAppDataPath]

    logging.info('Starting %(qosAppName)s' % locals())
    popenObj = subprocess.Popen(qoscmd)
    qos_pid = popenObj.pid
   
    logging.info("PID of QoS app is : " + str(qos_pid))
    
    #give time to QoS to initialize. hence sleep for 60sec
    time.sleep(300)

    #driverInitcmd = ['ycsb', 'load', 'mongodb', '-s', '-P',  'workloads/workloada', '>',  'outputLoad.txt']
    #driverInitcmd = ['ycsb', 'load', 'mongodb', '-s', '-P',  driverWorkload]
    #driverInitcmd = YCSB_DIR + "ycsb load mongodb -s -P " + driverWorkload
    currentDir = "/g/g90/mitra3/scheduling_work/LLNL-DCSL-PerformancePrediction/multi_app_with_qos/"
    driverInitcmd = currentDir + "mongoDB_by_ycsb.sh load " + driverWorkload

    print driverInitcmd


    try:
        # Ideally this call should not return untill driver loads all the data. check if that is the cas# for some reason this call is returning non-zero exit status 1 which throws exception. That is why this try-catch so that we can continue
    # for some reason this call is returning non-zero exit status 1 which throws exception. That is why this try-catch so that we can continue
        subprocess.check_call(driverInitcmd, shell=True)
    except subprocess.CalledProcessError:
        # Jason: Strongly recommend working around the exception via a retry or
        # fixing the underlying problem with ycsb load, instead of silently
        # ignoring the exception. Bad practice to ignore exceptions in general
        pass # do not do for CalledProcessError exception. 
    
    return qos_pid

def createQoSAppDataStorePath(output_path):
    qosDataStorePath = "/tmp/" + os.path.basename(output_path) + ".data"
    subprocess.check_call(['rm', '-rf', qosDataStorePath])
    subprocess.check_call(['mkdir', '-p', qosDataStorePath])
    return qosDataStorePath

def removeOldDir(dirToRemove):
    subprocess.check_call(['rm', '-rf', dirToRemove])

# Application format is '(suite bmark cores)+ output_path rep'
def run_experiment(params, output_path, rep):
    """
    old format (suite bmark #cores)+
    new format: (suite bmark #cores)+ (qosApp driverApp)
    """
    #print params
    #return

    applications = []                            # subrata need to save the benchmark results in a file. and pass the name of that file here
    for i in range(int((len(params) - 5) / 3)):  # subrata : parsing of the already created experiment list generated by "create_experiment.py"
        suite = params[3 * i]
        bmark = params[1 + 3 * i]
        cores = int(params[2 + 3 * i])
        applications.append([suite, bmark, cores])
    logging.info('Starting experiment with %d applications' % (len(applications)))
    
    qosApp = params[-5]
    driverApp = params[-4]
    driverWorkload = params[-3]

    # Cab contains 8 cores per SMP
    #reporter_core = 0    #subrata : reporter will be replaced by mongodB (interactive) => use two cores. YCSB will be in the other socket 2 cores anything between (8-15)
    qosApp_core = [0,1]    #subrata : specify the cores that qos app would use
    starting_core = 2
    ending_core = 7
    current_core = 2
    driver_core = [8,9]
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

    print applications
    # Pin ourself to the other socket
    #self_pin(ending_core+1)   # subrata : self pining of "this" python driver. similarly pin the benchmark driver YCSB/ apache bench etc. Pin tghem on the other socket to reduce intf
    self_pin(max_core)   # subrata : self pining of "this" python driver. similarly pin the benchmark driver YCSB/ apache bench etc. Pin tghem on the other socket to reduce intf
   
    #subrata: based on the already generated unique output path, create a temporary data store path for qos app (in /tmp/)
    dataStoreFileForQoS = createQoSAppDataStorePath(output_path)

    driverResultsPath = output_path + "_driver_output.txt"
    #now run and initialize the qos app...at the end of the experiment we will kill this qos app, so at this moment do not worry about the state 
    qos_pid = run_and_initialize_qos(qosApp, dataStoreFileForQoS, driverApp, qosApp_core, driverWorkload)

    ensure_data_dir()

    experiment = ".".join(['%(suite)s_%(bmark)s_%(cores)d' % locals() for suite, bmark, cores in applications])
    pid_file = './logs/%(experiment)s.%(rep)d.reporter.pid' % locals()    


    threads = []

    # Launch applications...
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

    reporter = None
    try:
        reporter = run_driver(output_path, pid_file, qosApp, qos_pid, driverApp, driver_core, driverWorkload, driverResultsPath) 
    except Exception as e:
        logging.exception("Error: Failed to start reporter")
        for thread in threads:
	    thread.exit()
        sys.exit(1)

    # TODO: Subrata : this is not the cleanest way to handle this. What would an abrupt exit do ?  It has created some other process...I am not sure how to handle the following
    # Kill the benchmark threads as the main thread running the driver has finished
    with lock:
        for key in procs:
            if procs[key] is not None:
                procs[key].kill()
                procs[key] = None    

    # Wait for threads to return
    for thread in threads:
        thread.join()
    
    # now also kill the qos application
    #subprocess.check_call('/bin/kill `/bin/cat %(pid_file)s`' % locals(), shell=True)
    
    #subrata: now kill the qos app as well. We will relaunch it during next experiment run

    subprocess.check_call('/bin/kill %(qos_pid)s' % locals(), shell=True)

    #subrata: now since this experiment has completed, remove the file used for data store
    removeOldDir(dataStoreFileForQoS)

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
    elif (len(sys.argv) - 3) % 3 == 0:
        # Parameters given on the command line
        run_experiment(sys.argv[1:], sys.argv[-2], int(sys.argv[-1]))
    else:
        print('Error: Invalid parameters')
        sys.exit(1)
