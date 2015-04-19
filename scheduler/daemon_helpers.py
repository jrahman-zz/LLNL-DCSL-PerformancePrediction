from flask import jsonify

from gevent import monkey
monkey.patch_all()

import httplib
import urllib2
import logging

DAEMON_PORT = 10000

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

def send_request(hostname, endpoint, method='GET', json=None):
	
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
	
