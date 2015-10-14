
import re
import math
import logging
import gevent.subprocess as subprocess
import gevent

def get_load():
	samples = 3

	# Grab a list of CPU cores for normalizing later
	cmd = ['lscpu']
	output = subprocess.check_output(cmd, stderr = subprocess.STDOUT)

	regex = r"CPU\(s\):\s*(\d+)"
	match = re.search(regex, output)
	if match is None:
		raise Exception('No match: %s' % (output))
	cpu_cores = int(match.group(1))

	memory = 0
	cores = 0
	for i in range(0, samples):
		memory = memory + get_free_memory()
		cores = cores + cpu_cores * get_idle_time()
		gevent.sleep(1)

	return {
		'cores': int(math.ceil(cores/samples)),
		'memory': memory / samples
	}

def get_free_memory():
	
	cmd = ['free', '-m']
	output = subprocess.check_output(cmd, stderr = subprocess.STDOUT)
	
	regex = r"Mem:\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)"
	match = re.search(regex, output)
	if match is None:
		raise Exception('No match: %s' % output)
	
	free = int(match.group(3))
	shared = int(match.group(4))
	buffers = int(match.group(5))
	cached = int(match.group(6))

	# http://blog.scoutapp.com/articles/2010/10/06/determining-free-memory-on-linux
	return free + shared + cached

def get_idle_time():

	cmd = ['top', '-b', '-n', '1']
	output = subprocess.check_output(cmd, stderr = subprocess.STDOUT)

	regex = r"Cpu\(s\): \s*(\d+\.\d+)\%us,\s*(\d+\.\d+)\%sy,\s*(\d+\.\d+)\%ni,\s*(\d+\.\d+)\%id,\s*(\d+\.\d+)\%wa,\s*(\d+\.\d+)\%hi,\s*(\d+\.\d+)\%si,\s*(\d+\.\d+)\%st"
	match = re.search(regex, output)
	if match is None:
		raise Exception('No match: %s' % output)

	user = float(match.group(1))/100
	system = float(match.group(2))/100
	nice = float(match.group(3))/100
	idle = float(match.group(4))/100
	wait = float(match.group(5))/100
	hw_inter = float(match.group(6))/100
	sw_inter = float(match.group(7))/100
	vm = float(match.group(8))/100

	return idle

def get_io_use():
	#snapshot_time             1428784316.174064
	#dirty_pages_hits          8969719
	#dirty_pages_misses        427289499
	#read_bytes                40839845
	#write_bytes               9654118
	#osc_read                  4986839
	#osc_write                 2037412
	#ioctl                     1333379
	#open                      3142149
	#close                     3142149
	#mmap                      12694
	#seek                      10557040
	#fsync                     4883
	#readdir                   259881
	#setattr                   1413491
	#truncate                  5657
	#getattr                   5705706
	#create                    379830
	#link                      8
	#unlink                    165500
	#symlink                   253
	#mkdir                     6915
	#rmdir                     22520
	#rename                    4686
	#statfs                    2221
	#alloc_inode               2258701
	#setxattr                  905
	#getxattr                  10891833
	#getxattr_hits             4514
	#listxattr                 3
	#removexattr               2
	#inode_permission          28202036

	#llstat /proc/fs/lustre/llite/lse-ffff88062a1dac00/stats
	pass	
