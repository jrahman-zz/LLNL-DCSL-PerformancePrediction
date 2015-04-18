
from flask import jsonify

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

