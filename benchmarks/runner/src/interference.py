
import logging
from gevent import Greenlet
from gevent import subprocess

class InterferenceThread(Greenlet):

    def __init__(self, cores=[0]):
        Greenlet.__init__(self)
        self._cores = cores
        self._process = None
        self._keep_running = True

    def __str__(self):
        return self._name

    def kill(self):
        self._stop()
        super(InterferenceThread, self).kill()

    def join(self):
        self._stop()
        super(InterferenceThread, self).join()

    def _stop(self):
        logging.debug('Stopping %s', self._name)
        if self._process is not None:
            self._process.kill()
        self._keep_running = False
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
                raise Exception('Process failure')

