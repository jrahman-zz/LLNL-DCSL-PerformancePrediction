#!/bin/env python

import subprocess
import time
import os
import signal

mpstat_core = 3
mpstat_period = 5
outfile_name = "abc_test"
cmd = 'taskset -c ' + str(mpstat_core) + ' mpstat -P 0,1,2,3,4,5,6,7 ' +  str(mpstat_period) + ' > ' + outfile_name

p = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

time.sleep(15)

print p.pid

#p.terminate()
#os.killpg(p.pid, signal.SIGKILL)
os.killpg(os.getpgid(p.pid), signal.SIGTERM)
