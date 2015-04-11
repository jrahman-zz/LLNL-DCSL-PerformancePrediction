import sys

import gevent
from gevent import monkey
monkey.patch_all()

if sys.version_info[0] == 3:
	from urllib.request import urlopen
else:
	from urllib2 import urlopen

if __name__ == "__main__":

	hostname = sys.argv[1]
	
	url = 'http://%s:%s/' % (hostname, 8000)
	data = urlopen(url).read()
	print(data)
