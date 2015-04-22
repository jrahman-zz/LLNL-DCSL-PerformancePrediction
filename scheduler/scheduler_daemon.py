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
@app.route(helpers.MEASUREMENT_UPDATE_ENDPOINT, methods=['POST'])
def update_measurements():
	message = request.json
	helpers.log_rpc(message)
	return jsonify(scheduler.update_measurements(message['data']))

"""
Receive worker status and load information
"""
@app.route(helpers.WORKER_UDPATE_ENDPOINT, methods=['POST'])
def update_worker():
	message = request.json
	helpers.log_rpc(message)
	return jsonify(scheduler.update_workers(message['data']))

"""
Receive notification that job status changed
"""
@app.route('/jobs/<int:id>', methods=['PUT'])
def job_update(id):
	message = request.json
	helpers.log_rpc(message)
	job_info = message['data']
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
		return jsonify(scheduler.update_job(self, id, job_info))
	except Exception as e:
		return internal_error(str(e))

"""
Submit a job for scheduling
"""
@app.route(helpers.JOB_SUBMIT_ENDPOINT, methods=['POST'])
def submit_jobs():
	message = request.json
	helpers.log_rpc(message)
	return jsonify(scheduler.queue_jobs(message['data']))

"""
Get the schedulers global status
"""
@app.route(helper.SCHEDULER_STATUS_ENDPOINT, methods=['GET'])
def get_status():
	return jsonify(scheduler.get_status())

# Configure error handlers
@app.errorhandler(404)
def not_found_error(e):
	helper.not_found(e.args[0])

@app.errorhandler(ValueError)
def value_error(e):
	helper.bad_request(e.args[0])

if __name__ == '__main__':
	
	policy = sys.argv[1].lower()
	if policy == 'least_loaded':
		scheduler = LeastLoaded()
	else:
		scheduler = LeastLoaded()

	server = WSGIServer(('', helpers.DAEMON_PORT), app)
	server_greenlet = gevent.spawn(WSGIServer.serve_forever, server)

	while True:
		gevent.sleep(1.0/helpers.SCHEDULER_HERTZ)
		scheduler.scheduling_pass()
	
	server.greenlet.join()
