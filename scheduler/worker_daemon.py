import sys
import logging
import os

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

@app.route('/job/start', methods=['POST'])
def start_job():
	return local_id

# Configure error handlers
@app.errorhandler(404)
def not_found_error(e):
    helper.not_found(e.args[0])

#@app.errorhandler(ValidationError)
#def validation_error(e):
#    helper.bad_request(e.args[0])


def notify_master():
	processors = subprocess.check_output('cat /proc/cpuinfo | grep processor | wc -l', shell=True)
	
	message = {}
	message['hostname'] = os.environ['HOSTNAME']
	message['processors'] = int(processors)
	message['memory'] = get_load.get_free_memory()
	message['time'] = datetime.utcnow()

	response = helpers.send_request(sys.argv[1], '/worker/update', json.dumps(message))

if __name__ == '__main__':

	logging.basicConfig(level=logging.INFO)

	logging.info('Starting server...')
	server = WSGIServer(('', 8000), app)
	server_greenlet = gevent.spawn(WSGIServer.serve_forever, server)
	
	gevent.sleep(1)

	notify_master()

	# TODO, status polling and measurement polling loop here

	server_greenlet.join()
