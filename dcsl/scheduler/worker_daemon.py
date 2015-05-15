import sys
import logging
import os

import signal

from datetime import datetime

from flask import Flask, jsonify, request, json

import get_load
import daemon_helpers as helpers
from job_manager import JobManager
from measurement_manager import MeasurementManager

import argparse
import logging
import gevent
from gevent.pywsgi import WSGIServer
from gevent import subprocess

from automation.load_environ import load_environ

app = Flask(__name__)

# Yes, globals, evil, I know
environ = None
job_manager = None
measurement_manager = None

total_memory = None
total_processors = None

def measurement():
	""" Perform a status measurement """
	measurement = get_load.get_load()
	response = helpers.update_worker(environ['master'], message)

def job_completed(job_type, job_id, start_time, end_time, exit_code):
	""" Take action when a job completes according to the job manager """
	# TODO
	pass

def init_server(args):
	global environ
	global job_manager
	global measurement_manager

	base_path = args.config_path
	modules = args.modules
	master = args.master	

	modules = ['%s/%s' % (base_path, module) for module in modules]
	environ = load_environ('%s/config.json' % (base_path), modules)

	if master != '':
		environ['master'] = master

	job_manager = JobManager(environ)
	job_manager.register_completion_cb(job_completed)
	measurement_manager = MeasurementManager(environ)
	

@app.route('/')
def root():
	return "Hello"

@app.route(helpers.JOB_START_ENDPOINT, methods=['POST'])
def start_job():
	message = request.json
	helpers.log_rpc(message)
	data = message['data']
	return job_manager.start_job(data)

@app.route(helpers.WORKER_UPDATE_ENDPOINT, methods=['GET'])
def worker_update():
	# Takes three samples over three seconds
	load = get_load.get_load()
	jobs = job_manager.get_running_jobs()
	data = build_update_message(load['cores'], load['memory'], jobs)
	message = helpers.create_message('update_worker')
	message['data'] = data
	return jsonify(message)
	

# Configure error handlers
@app.errorhandler(404)
def not_found_error(e):
    helper.not_found(e.args[0])

@app.errorhandler(ValueError)
def value_error(e):
	helper.bad_request(e.args[0])

keep_alive = True

def signal_handler(signo, stack):
	global keep_alive
	if keep_alive:
		keep_alive = False
	else:
		sys.exit(1)

#@app.errorhandler(ValidationError)
#def validation_error(e):
#    helper.bad_request(e.args[0])

def build_update_message(avail_processors, avail_memory, running_jobs):
	global total_processors
	global total_memory
	message = {}
	message['total_processors'] = total_processors
	message['free_processors'] = avail_processors
	message['total_memory'] = total_memory
	message['free_memory'] = avail_memory
	message['hostname'] = os.getenv('HOSTNAME')
	message['running_jobs'] = running_jobs
	return message


def notify_master():
	""" Indicate that we have just started normal operation """
	global total_processors
	global total_memory
	procs = subprocess.check_output('cat /proc/cpuinfo | grep processor | wc -l', shell=True)
	total_processors = int(procs)
	total_memory = get_load.get_free_memory()
	running_jobs = job_manager.get_running_jobs()
	message = build_update_message(total_processors, total_memory, running_jobs)
	response = helpers.update_worker(environ['master'], message)

	

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--master', type=str, help='Hostname for the master node', default='')
	parser.add_argument('--measurements', type=bool, help='1 to record microbenchmarks')
	parser.add_argument('--modules', type=str, nargs='*', help='Additional configuration modules', default=['benchmarks.json', 'applications.json'])
	parser.add_argument('--config_path', type=str, help='Path to config folder', default='.')
	return parser.parse_args()

def main():
	signal.signal(signal.SIGTERM, signal_handler)
	logging.basicConfig(level=logging.INFO)

	logging.info('Worker: Initializing...')
	args = get_args()
	init_server(args)
	logging.info('Worker: Initialized')
	
	logging.info('Worker: Starting...')
	server = WSGIServer(('', 8000), app)
	server_greenlet = gevent.spawn(WSGIServer.serve_forever, server)
	
	gevent.sleep(1)

	# Tell the master that we are ready to begin running jobs
	notify_master()

	delta = 0.5
	while keep_alive:
		for i in range(0, int(helpers.MEASUREMENT_LOOP_DELAY/delta)):
			gevent.sleep(delta)
		measurement()
		
	server_greenlet.join()

if __name__ == '__main__':
	main()
