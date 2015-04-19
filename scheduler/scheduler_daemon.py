import sys

from flask import Flask, jsonify, request
#/from flask.ext.wtf import ValidationError
import daemon_helpers as helpers

import gevent
from gevent.pywsgi import WSGIServer

from policies.least_loaded import LeastLoaded

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
def update_worker():
	worker = request.json
	scheduler.update_workers(workers)
	return 200

"""
Receive notification that job status changed
"""
@app.route('/jobs/<int:id>', methods=['PUT'])
def job_update(id):
	job_info = request.json
	if not job_info or not 'status' in job_info:
		return bad_request('Invalid job status message')

	if job_info['status'] == JobState.Completed:
		logging.info('Job: %s completed at %s',
								job_info['id'],
								job_info['end_time'])
	elif job_info['status'] == JobState.Failed:
		logging.info('Job: %s failed at %s, Output: %s',
								job_info['id'],
								job_info['end_time'],
								job_info['output'])
	else:
		logging.info('Job: %s started at %s',
								job_info['id'],
								job_info['start_time'])

	try:
		scheduler.update_job(self, id, job_info)
		return 200
	except Exception as e:
		return internal_error(str(e))

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
@app.route('/status', methods=['GET'])
def get_status():
	return scheduler.get_status()

# Configure error handlers
@app.errorhandler(404)
def not_found_error(e):
	helper.not_found(e.args[0])

#@app.errorhandler(ValidationError)
#def validation_error(e):
#	helper.bad_request(e.args[0])

if __name__ == '__main__':
	
	policy = sys.argv[1].lower()
	if policy == 'least_loaded':
		scheduler = LeastLoaded()
	else:
		scheduler = LeastLoaded()

	server = WSGIServer(('', helpers.DAEMON_PORT), app)
	server_greenlet = gevent.spawn(WSGIServer.serve_forever, server)

	# TODO, scheduler impl here
	while True:
		gevent.sleep(1)
		scheduler.scheduling_pass()
	
	server.greenlet.join()
