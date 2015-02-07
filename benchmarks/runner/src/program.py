
import sys
import gevent.greenlet as greenlet
import gevent.subprocess as subprocess

class Program(greenlet.Greenlet):

    def __init__(self, cores=[0]):
        greenlet.Greenlet.__init__(self)
        self._cores = cores

    def __str__(self):
        return self._name

    def _run(self):
        self._setup()
        cores = ','.join(map(lambda x: str(x), self._cores))

        cmd = ['taskset', '-c', cores, self._cmd]
        cmd = cmd + self._params
        
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        output = self._process_output(output)
        self._teardown()
        return output

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):
        pass

