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
        try:
            self._stop()
            Greenlet.kill(self, timeout)
        except OSError as e:
            logging.exception('Failed to stop interference, errno: %d', e.errno)
            raise
        except Exception as e:
            logging.exception('Failed to stop interference: %s', str(e))
            raise

    def join(self, timeout = None):
        try:
            self._stop()
            Greenlet.join(self, timeout)
        except OSError as e:
            logging.exception('Failed to stop interference, errno: %d', e.errno)
            raise
        except Exception as e:
            logging.exception('Failed to stop interference: %s', str(e))
            raise

    def _stop(self):
        logging.info('Stopping %s', self._name)
        self._keep_running = False
        process = self._process
        self._process = None
        if process is not None:
           try:
              process.kill()
           except OSError as e:
              logging.exception('Failed to kill interference')

    def _run(self):
        try:
            from subprocess import DEVNULL # py3
        except ImportError:
            import os
            DEVNULL = open(os.devnull, 'wb')
        cores = ','.join(map(lambda x: str(x), self._cores))
        args = ['taskset', '-c', cores, 'nice', '-n', str(self._nice), self._cmd] + self._params
        prog = args[6].split('/')[-1]
        while self._keep_running:
            logging.info('Starting new %s process...', prog)
            self._process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            return_code = self._process.wait()
            logging.info('Interference process %s exited with return code %d', prog, return_code)
            
            # Return code of -9 means SIGKILL, this is OK!
            if not (return_code == 0 or return_code == -9):
                self._keep_running = False
                self._obj._teardown()
                (stdout, _) = self._process.communicate()
                raise Exception('Process failure, return code %d: %s' % (return_code, stdout))
        
        # Set ourself to None so that _stop doesn't try to do anything
        # with a completed process
        self._obj._teardown()
        self._process = None

