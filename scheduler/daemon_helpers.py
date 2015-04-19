from flask import jsonify, json

from gevent import monkey
monkey.patch_all()

import httplib
import urllib2
import logging

# Schedule every 2 seconds
SCHEDULER_HERTZ = 0.25

DAEMON_PORT = 10000
MEASUREMENT_LOOP_DELAY = 15

JOB_START_ENDPOINT = '/job/start'
JOB_SUBMIT_ENDPOINT = '/job/submit'
WORKER_UPDATE_ENDPOINT = '/worker/update'
MEASUREMENT_UPDATE_ENDPOINT = '/measurements/update'
SCHEDULER_STATUS_ENDPOINT = '/status'

def bad_request(message):
	response = jsonify({'error': 'bad request', 'message': message})
	response.status_code = 400
	return response

def not_found(message):
	response = jsonify({'error': 'not found', 'message': message})
	response.status_code = 404
	return response

def internal_error(message):
	response = jsonify({'error': 'internal error', 'message': message})
	response.status_code = 500
	return response

def send_request(hostname, endpoint, json=None):
	
	url = '%s:%s' % (hostname, DAEMON_PORT)

	logging.info('Hostname: %s', url)
	
	conn = httplib.HTTPConnection(url)
	
	fullurl = "http://%s/%s" % (url, endpoint)
	if not json is None:
		headers = {'Content-Type': 'application/json'}
		conn.request(method, endpoint, json)
		#req = urllib2.Request(url=fullurl, data=json)
		#req.add_header('Content-Type', 'application/json')
	else:
		#req = urllib2.Request(url=fullurl)
		conn.request(method, endpoint)
	#f = urllib2.urlopen(req)

	response = conn.getresponse()
	return response

def log_rpc(message):
	logging.info('Message: %s from %s sent at %s', message['type'], message['hostname'], message['time'])

def create_message(type):
	message = {}
	message['type'] = type
	message['hostname'] = os.environ['HOSTNAME']
	message['time'] = datetime.utcnow()
	return message

def start_job(hostname, jobtype):
	message = create_message('start_job')
	message['data'] = {'jobname': jobtype}
	return send_request(hostname, JOB_START_ENDPOINT, json.dumps(message))

def update_worker(hostname, info):
	message = create_message('update_worker')
	message['data'] = info
	return send_request(hostname, WORKER_UPDATE_ENDPOINT, json.dumps(message))

def submit_jobs(hostname, jobs):
	message = create_message('submit_jobs')
	message['data'] = jobs
	return send_request(hostname, JOB_SUBMIT_ENDPOINT, json.dumps(message))

def update_measurement(hostname, measurement):
	message = create_message('update_measurement')
	message['data'] = measurement
	return send_request(hostname, MEASUREMENT_UPDATE_ENDPOINT, json.dumps(message))
	
def update_job(hostname, job_info, id):
	message = create_message('update_job')
	message['data'] = job_info
	return send_request(hostname, '/job/%s' % (id), json.dumps(message))
