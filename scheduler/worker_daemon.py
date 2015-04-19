import sys
import logging
import os

import signal

import get_load
from datetime import datetime

from flask import Flask, jsonify, request, json
import daemon_helpers as helpers

import gevent
from gevent.pywsgi import WSGIServer
from gevent import subprocess

app = Flask(__name__)

@app.route('/')
def root():
	return "Hello"

@app.route(helpers.START_JOB_ENDPOINT, methods=['POST'])
def start_job():
	# TODO
	return local_id

# Configure error handlers
@app.errorhandler(404)
def not_found_error(e):
    helper.not_found(e.args[0])

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
	processors = subprocess.check_output('cat /proc/cpuinfo | grep processor | wc -l', shell=True)
	
	message = {}
	message['processors'] = int(processors)
	message['memory'] = get_load.get_free_memory()

	response = helpers.update_worker(sys.argv[1], message)

def measurement():
	measurement = get_load.get_load()
	response = helpers.update_worker(sys.argv[1], message))

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
