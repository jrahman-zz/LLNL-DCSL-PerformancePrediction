
import os
import logging
from gevent import Greenlet, GreenletExit
from gevent import subprocess

class InterferenceThread(Greenlet):

    def __init__(self, environ, cores=[0]):
        Greenlet.__init__(self)
        self._cores = cores
        self._process = None
        self._keep_running = True
        self._benchmark_dir = environ['benchmark_dir']


    # Use context manager for use in with statement
    def __enter__(self):
        print 'In enter'
        self.start()

    def __exit__(self, type, value, traceback):
        print 'In exit'
        self.join()

    def __str__(self):
        return self._name

    def kill(self, exception = GreenletExit, block = True, timeout = None):
        self._stop()
        Greenlet.kill(self, exception, block, timeout)

    def join(self, timeout = None):
        self._stop()
        Greenlet.join(self, timeout)

    def _stop(self):
        logging.info('Stopping %s', self._name)
        self._keep_running = False
        if self._process is not None:
            self._process.kill()
        self._process = None


    def _run(self):
        try:
            from subprocess import DEVNULL # py3
        except ImportError:
            import os
            DEVNULL = open(os.devnull, 'wb')

        cores = ','.join(map(lambda x: str(x), self._cores))
        args = ['taskset', '-c', cores, self._cmd] + self._params
        prog = args[3].split('/')[-1]
        while self._keep_running:
            logging.info('Starting new %s process...', prog)
            self._process = subprocess.Popen(args, stdout=DEVNULL, stderr=subprocess.STDOUT)
            return_code = self._process.wait()
            logging.info('Interference process %s exited with return code %d', prog, return_code)
            
            # Return code of -9 means SIGKILL, this is OK!
            if not (return_code == 0 or return_code == -9):
                self._keep_running = False
                raise Exception('Process failure, return code %d' % (return_code))
        
        # Set ourself to None so that _stop doesn't try to do anything
        # with a completed process
        self._process = None

