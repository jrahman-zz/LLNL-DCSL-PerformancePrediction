
import logging
import gevent.greenlet as greenlet
import gevent.subprocess as subprocess

class Application():

    def __init__(self, environ, application_name, start_cores, run_cores):
        
        # Basic information for an application module
        self._application_name = application_name
        self._script_dir = environ['applications'][self._application_name]['script_dir']
        self._application_dir = environ['applications'][self._application_name]['application_dir']
        self._data_dir = environ['data_dir']

        self._interface_params = [self._application_dir, self._data_dir]

        # TODO, clarify how this works
        self._run_cores = run_cores
        self._start_cores = start_cores
        
        self._loaded = False
        self._started = False
        
        # Extra params that the sub-class will provide for it's shell automation scripts
        self._load_params = []
        self._start_params = []
        self._run_params = []
        self._stop_params = []
        self._cleanup_params = []
        self._interfere_params = []

    def __str__(self):
        return self._application_name

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    def load(self):
        """ Load data ahead of any potential benchmark run """
        if self._started or self._loaded:
            raise ValueError('Already loaded or started')

        cmd = ["%s/load.sh" % (self._script_dir)]
        cmd = cmd + self._interface_params
        cmd = cmd + self._load_params

        logging.info('Loading application: %s', str(self))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT )
        except subprocess.CalledProcessError as e:
            logging.error('Loading application %s failed, output: %s', str(self), e.output)
            raise

        self._loaded = True

    # TODO, improve to use the with ... as ... idiom

    def start(self):
        """ Start and run the actual benchmark """
        if self._started or not self._loaded:
            raise ValueError('Not started or already loaded')

        cores = ','.join(map(lambda x: str(x), self._start_cores))
        cmd = ['taskset', '-c', cores]
        cmd = cmd + ["%s/start.sh" % (self._script_dir)]
        cmd = cmd + self._interface_params
        cmd = cmd + self._start_params

        logging.info('Starting application: %s', str(self))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logging.error('Failed to start application %s, output: %s', str(self), e.output)
            raise

        self._started = True

    def interfere(self):
        if not self._started or not self._loaded:
            raise ValueError('Not started or loaded yet')

        # Create list of allowable cores
        cores = ','.join(map(lambda x: str(x), self._run_cores))

        # Build the command
        cmd = ['taskset', '-c', cores]
        cmd = cmd + ['%s/run.sh' % (self._script_dir)]
        cmd = cmd + self._interface_params
        cmd = cmd + self._interfere_params

        return BackgroundProcess(cmd, self._application_name)

    def run(self): 
        """ Run the actual app which generates parseable output """
        if not self._started or not self._loaded:
            raise ValueError('Not started or loaded yet')
            
        # Create list of cores we are allowed to run on
        cores = ','.join(map(lambda x: str(x), self._run_cores))

        # Build our command as required
        cmd = ['taskset', '-c', cores]
        cmd = cmd + ["%s/run.sh" % (self._script_dir)]
        cmd = cmd + self._interface_params
        cmd = cmd + self._run_params

        # Run the command and process the output as needed
        logging.info('Running application: %s', str(self))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logging.error('Failed to run application %s, output: %s', str(self), e.output)
            raise

        features = self._process_output(output)
        return features

    def stop(self):
        """ Stop any benchmark background operations """
        if not self._started:
            # TODO, raise error here
            pass

        cmd = ["%s/stop.sh" % (self._script_dir)]
        cmd = cmd + self._interface_params
        cmd = cmd + self._stop_params

        logging.info('Stopping application: %s', str(self))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logging.error('Failed to stop application %s, output %s', str(self), e.output)
            raise

        self._started = False

    def cleanup(self):
        """ Perform any final cleanup needed """
        if self._loaded == False:
            # TODO, raise error here
            pass

        cmd = ["%s/cleanup.sh" % (self._script_dir)]
        cmd = cmd + self._interface_params
        cmd = cmd + self._cleanup_params

        logging.info('Cleaning up application: %s', str(self))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logging.error('Failed to cleanup application %s, output %s', str(self), e.output)
            raise

        self._loaded = False

    def _process_output(self, output):
        pass

class BackgroundProcess(greenlet.Greenlet):

    def __init__(self, args, application_name):
        greenlet.Greenlet.__init__(self)
        self._args = args
        self._application_name
        self._keep_running = True

    def __str__(self):
        return self._application_name

    # Implement __enter__ and __exit__ so we can use with
    def __enter__(self):
        self.start()        
    
    def __exit__(self, type, value, traceback):
        self.join()
    
    def kill(self, exception=greenlet.GreenletExit, block = True, timeout = None):
        self._stop()
        greenlet.Greenlet.kill(self, exception, block, timeout)


    def join(self, timeout = None):
        self._stop()
        return greenlet.Greenlet.join(self, timeout)

    def _stop(self):
        logging.debug('Stopping application %s', self._application_name)
        self._keep_running = False
        if self._process is not None:
            self._process.kill()
        self._process = None

    def _run(self):
        try:
            from subprocess import DEVNULL
        except ImportError:
            import os
            DEVNULL = open(os.devnull, 'wb')
    
        prog = self._args[3].split('/')[-1]
        while self._keep_running:
            logging.info('Starting new %s process...', prog)
            self._process = subprocess(self._args, stdout=DEVNULL, stderr=subprocess.STDOUT)
            return_code = self._process.wait()
            logging.info('Interference application %s exited with return code %d', prog, return_code)
        
            # Return code of -9 means SIGKILL, this is ok
            if not (return_code == 0 or return_code == -9):
                self._keep_running = False
                raise Exception('Process failure, return code %d' % (return_code))
            
        self._process = None
