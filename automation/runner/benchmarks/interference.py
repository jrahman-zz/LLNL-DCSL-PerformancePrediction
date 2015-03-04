
import os
import logging
from gevent import Greenlet, GreenletExit
from gevent import subprocess

class Interference:
    def __init__(self, environ, cores=[0], nice=0):
        self._nice = nice
        self._cores = cores
        self._benchmark_dir = environ['benchmark_dir']
        self._data_dir = environ['data_dir']

    def __hash__(self):
        return hash(str(self))
    
    def __str__(self):
        return self._name

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    def load(self):
        pass

    def start(self):
        pass

    def interfere(self):
        return InterferenceThread(self, self._cmd, self._params, self._name, self._cores, self._nice)

    def stop(self):
        pass

    def cleanup(self):
        pass

    def _teardown(self):
        pass

class InterferenceThread(Greenlet):

    def __init__(self, obj, cmd, params, name, cores=[0], nice=0):
        Greenlet.__init__(self)
        self._obj = obj
        self._nice = str(nice)
        self._cores = cores
        self._process = None
        self._keep_running = True
        self._cmd = cmd
        self._params = params
        self._name = name

    # Use context manager for use in with statement
    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.join()

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
        args = ['nice', '-%s' % (self._nice), 'taskset', '-c', cores, self._cmd] + self._params
        prog = args[5].split('/')[-1]
        while self._keep_running:
            logging.info('Starting new %s process...', prog)
            self._process = subprocess.Popen(args, stdout=DEVNULL, stderr=subprocess.STDOUT)
            return_code = self._process.wait()
            logging.info('Interference process %s exited with return code %d', prog, return_code)
            
            # Return code of -9 means SIGKILL, this is OK!
            if not (return_code == 0 or return_code == -9):
                self._keep_running = False
                self._obj._teardown()
                raise Exception('Process failure, return code %d' % (return_code))
        
        # Set ourself to None so that _stop doesn't try to do anything
        # with a completed process
        self._obj._teardown()
        self._process = None

