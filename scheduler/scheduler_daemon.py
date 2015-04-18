import sys

from flask import Flask, jsonify, request
import daemon_helpers as helpers

import gevent
from gevent.pyqsgi import WSGIServer

app = Flask(__name__)

scheduler = None

"""
Receive worker enviroment measurement information
"""
@app.route('/measurements/update', methods=['POST'])
def update_measurements():
	pass

"""
Receive worker status and load information
"""
@app.route('/worker/update', methods=['POST'])
def update_status():
	# TODO, deser the body
	workers = None
	scheduler.update_workers(workers)
	# TODO, return value

"""
Receive notification that a job ended
"""
@app.route('/jobs/<int:id>', methods=['POST'])
def finished_job(id):
	# TODO, deser the job info
	job_info = None
	try:
		scheduler.update_job(self, id, job_info)
		return 200

"""
Submit a job for scheduling
"""
@app.route('/jobs/submit', methods=['POST'])
def schedule_jobs():
	# TODO, deser the jobs from the request body
	jobs = None
	return jsonify(scheduler.queue_jobs(jobs))

"""
Get the schedulers global status
"""
@app.route('/status', methods=['GET']
def get_status():
	return scheduler.get_status()

# Configure error handlers
@app.errorhandler(404)
def not_found_error(e):
	helper.not_found(e.args[0])

@app.errorhandler(ValidationError)
def validation_error(e):
	helper.bad_request(e.args[0])

if __name__ == '__main__':
	
	# TODO, init scheduler

	server = WSGIServer(('', 8000), app)
	server_greenlet = gevent.spawn(WSGIServer.serve_forever, server)

	# TODO, scheduler impl here
	while True:
		scheduler.scheduling_pass()
	
	server.greenlet.join()
