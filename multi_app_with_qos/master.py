
import logging
import time
import socket
import sys
import functools

from flask import Flask, request
app = Flask(__name__)

experiment_deadline_s = 120 * 60 # 120 minutes

def with_file(filename, mode='r'):
    """
    Decorator generating function for wrapping a function
    invocation around a given file and mode
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with open(filename, mode) as f:
                function = functools.partial(func, f)
                return function(*args, **kwargs)
        return wrapper
    return decorator

def deserialize_experiment(experiment):
    values = experiment.split()
    if (len(values) - 2) % 3 != 0:
        raise Exception('Invalid experiment: %(experiment)s' % experiment)
    parsed_experiment = {'rep': int(values[-1]), 'data_path': values[-2]}
    parsed_experiment['apps'] = [{'suite': values[3*i], 'bmark': values[3*i+1],'cores': int(values[3*i + 2])} for i in range(len(values) / 3)]
    return parsed_experiment

def serialize_experiment(experiment):
    string = " ".join([" ".join[app['suite'], app['bmark'], app['cores']] for app in experiment['apps']])
    string += " ".join([experiment['data_path'], experiment['rep']])
    return string
        
@with_file('experiment_list', 'r')
def read_experiment_list(f):
    logging.info('Reading experiments from experiment_list...')
    experiments = [experiment.strip() for experiment in f if len(experiment.strip()) > 0]
    logging.info('Read %d experiments from experiment_list' % len(experiments))
    return experiments

@with_file('completed_experiments', 'r+')
def read_completed_experiments(f):
    logging.info('Reading completed experiments from file...')
    experiments = set([experiment.strip() for experiment in f if len(experiment.strip()) > 0])
    logging.info('Read %d completed experiments from file' % len(experiments))
    return experiments

@with_file('completed_experiments', 'w')
def write_completed_experiments(f, completed_experiments):
    logging.info('Writing %d completed experiments to file...', len(completed_experiments))
    for experiment in completed_experiments:
        f.write('%(experiment)s\n' % locals())
    f.flush()
    logging.info('Wrote %d completed experiments to file', len(completed_experiments))

# List of experiments
ready_experiments = []

# Dictionary of start_time => experiment_dictionary
pending_experiments = dict()

# Dictionary of experiment_key => start_time values
running_experiments = dict()

# 
completed_experiments = set()
    
def expire_pending_experiments():
    global pending_experiments
    global ready_experiments
    current_time = time.time()
    logging.info('Checking for expired experiments at time %(current_time)d' % locals())
    for start_time, experiments in pending_experiments.items():
        if start_time + experiment_deadline_s > current_time:
            experiment_count = len(experiments)
            logging.info('Expiring %(experiment_count)d experiments' % locals())
            ready_experiments += experiments

def add_completed_experiment(experiment):
    global completed_experiments
    completed_experiments.add(experiment)
    write_completed_experiments(completed_experiments)

def experiment_complete(experiment):
    global ready_experiments
    global running_experiments
    global pending_experiments
    
    logging.info('Experiment: %(experiment)s completed' % locals())
    # Remove key from ready experiments if needed
    if experiment in ready_experiments:
        ready_experiments.remove(experiment)
    if experiment in running_experiments:
        start_time = running_experiments[experiment]
        pending_experiments[start_time].remove(experiment)
        del running_experiments[experiment]
    add_completed_experiment(experiment)
   
def init_experiments():
    global completed_experiments
    global pending_experiments
    global running_experiments
    global ready_experiments

    completed_experiments = completed_experiments.union(read_completed_experiments())
    ready_experiments += read_experiment_list()
    for experiment in completed_experiments:
        if experiment in ready_experiments:
            ready_experiments.remove(experiment)
    logging.info('%d experiments already complete' % len(completed_experiments))
    logging.info('%d experiments ready to run' % len(ready_experiments))
        

def get_next_experiment():
    global ready_experiments
    logging.info('%d experiments ready to run' % len(ready_experiments))
    if len(ready_experiments) == 0:
        expire_pending_experiments()
    if len(ready_experiments) == 0:
        raise Exception('No experiments left')
    experiment = ready_experiments[0]
    del ready_experiments[0]
    return experiment

def mark_experiment_started(experiment):
    global running_experiments
    global pending_experiments
    start_time = time.time()
    if start_time not in pending_experiments:
        pending_experiments[start_time] = []
    pending_experiments[start_time].append(experiment)
    running_experiments[experiment] = start_time

def print_status():
    global ready_experiments
    global running_experiments
    global completed_experments
    ready = len(ready_experiments)
    running = len(running_experiments)
    complete = len(completed_experiments)
    logging.info('Ready experiments: %(ready)d, running experiments: %(running)d, completed experiments: %(complete)d' % locals())

@app.route('/get_experiment', methods=['GET'])
def get_new_experiment():
    try:
        experiment = get_next_experiment()
        mark_experiment_started(experiment)
        print_status()
        logging.info('Sending experiment: %(experiment)s' % locals())
        return experiment, 200
    except Exception as e:
        logging.exception('Failed to retrieve experiment: %s' % str(e))
        return str(e), 500
        
@app.route('/return_experiment', methods=['POST'])
def return_completed_experiment():
    result = request.get_json(force=True)
    if result['success']:
        experiment_complete(result['experiment'].strip())
    else:
        # TODO
        pass
    print_status()
    return "SUCCESS", 200

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    init_experiments()
    app.run(host=socket.gethostname(), port=int(sys.argv[1]))
