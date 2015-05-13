import sys

from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def root():
	return "Hello"


if __name__ == '__main__':
	server = WSGIServer(('', 8000), app)
	server.serve_forever()
