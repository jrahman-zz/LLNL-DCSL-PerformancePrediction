import sys

from flask import Flask, jsonify, request
import daemon_helpers as helpers

import gevent
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def root():
	return "Hello"

@app.route('/job/start', methods=['POST'])
def start_job():
	return local_id

#@app.route('/job/kill/<int:id>', methods=['POST'])
#def kill_job(id)
	jobs[str(id)].kill()

# Configure error handlers
@app.errorhandler(404)
def not_found_error(e):
    helper.not_found(e.args[0])

@app.errorhandler(ValidationError)
def validation_error(e):
    helper.bad_request(e.args[0])


if __name__ == '__main__':

	server = WSGIServer(('', 8000), app)
	server_greenlet = gevent.spawn(WSGIServer.serve_forever, server)
	
	for i in range(0, 100):
		print("Hello")
		gevent.sleep(1)

	# TODO, status polling and measurement polling loop here

	server_greenlet.join()
