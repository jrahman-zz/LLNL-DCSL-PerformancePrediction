
import sys
import os
import logging
import gevent.greenlet as greenlet
import gevent.subprocess as subprocess

class Benchmark(greenlet.Greenlet):

    def __init__(self, environ, cores=[0]):
        greenlet.Greenlet.__init__(self)
        self._cores = cores
        self._benchmark_dir = environ['benchmark_dir']

    def __str__(self):
        return self._name

    def _run(self):
        self._setup()
        cores = ','.join(map(lambda x: str(x), self._cores))

        cmd = ['taskset', '-c', cores, self._cmd]
        cmd = cmd + self._params
        features = {}

        logging.info('Starting benchmark %s', str(self))

        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            
            logging.info('Finished running benchmark %s', str(self))
            
            features = self._process_output(output)
        except:
            # Teardown for cleanup, then rethrow for capture somewhere else
            self._teardown()
            raise
        return features

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):
        pass

