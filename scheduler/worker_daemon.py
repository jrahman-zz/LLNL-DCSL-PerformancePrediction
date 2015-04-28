import sys
import logging
import os

import signal

from datetime import datetime

from flask import Flask, jsonify, request, json

import scheduler.get_load
import scheduler.daemon_helpers as helpers
from scheduler.job_manager import JobManager
from scheduler.measurement_manager import MeasurementManager

import gevent
from gevent.pywsgi import WSGIServer
from gevent import subprocess

import automation.runner.load_environ

app = Flask(__name__)

def measurement():
	""" Perform a status measurement """
	measurement = get_load.get_load()
	response = helpers.update_worker(sys.argv[1], message))

def job_completed(job_type, job_id, start_time, end_time, exit_code):
	""" Take action when a job completes according to the job manager """
	# TODO
	pass

environ = None
job_manager = None
measurement_manager = None

def init_server(base_path, modules):
	global environ
	global job_manager
	global measurement_manager

	modules = ['%s/%s' % (base_path, module) for module in modules]
	environ = load_environ('%s/config.json' % (base_path), modules)
	job_manager = JobManager(environ)
	job_manager.register_completion_cb(job_completed)
	measurement_manager = MeasurementManager(environ)
	

@app.route('/')
def root():
	return "Hello"

@app.route(helpers.START_JOB_ENDPOINT, methods=['POST'])
def start_job():
	message = request.json
	helpers.log_rpc(message)
	data = message['data']
	return job_manager.start_job(data)

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


def notify_master():
	""" Indicate that we have just started normal operation """
	processors = subprocess.check_output('cat /proc/cpuinfo | grep processor | wc -l', shell=True)
	message = {}
	message['processors'] = int(processors)
	message['memory'] = get_load.get_free_memory()
	response = helpers.update_worker(sys.argv[1], message)

if __name__ == '__main__':
	signal.signal(signal.SIGTERM, signal_handler)
	logging.basicConfig(level=logging.INFO)

	logging.info('Starting server...')
	server = WSGIServer(('', 8000), app)
	server_greenlet = gevent.spawn(WSGIServer.serve_forever, server)
	
	gevent.sleep(1)

	notify_master()

	delta = 0.5
	while keep_alive:
		for i in range(0, int(helpers.MEASUREMENT_LOOP_DELAY/delta)):
			gevent.sleep(delta)
		measurement()
		
	server_greenlet.join()
