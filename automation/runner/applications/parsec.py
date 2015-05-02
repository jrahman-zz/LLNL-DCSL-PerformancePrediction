from application import Application
import math
import logging
import re

class Parsec(Application):

    def __init__(self, environ, app_cores, client_cores, size, nice=0, instance=1):
        Application.__init__(self, environ, 'Parsec', client_cores, app_cores, nice, instance)
        self._load_params = [self._bmark_name]
        self._cleanup_params = [self._bmark_name]
        self._run_params = [self._bmark_name, size, str(self._run_core_count)]
        self._intefere_params = [self._bmark_name, size,  str(self._run_core_count)]

    def _process_output(self, output):
        regex = r"real\s+(\d+)m(\d+\.\d+)s"
        match = re.search(regex, output)
        if match is None:
            logging.warning('Mismatch: %s', output)
            raise Exception('No match')
        features = {
            'time': 60 * float(match.group(1)) + float(match.group(2))
        }
        return features

    def __str__(self):
        return "parsec_%s" % (self._bmark_name)


class ParsecBlackscholes(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'blackscholes'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecBodytrack(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'bodytrack'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecCanneal(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'canneal'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecDedup(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'dedup'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecFacesim(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'facesim'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecFerret(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'ferret'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecFluidanimate(Parsec):
    # Note, needs power of 2 for core count
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'fluidanimate'
        # Cores must be power of 2
        power = int(math.log(len(app_cores), 2) + 0.5)
        if 2 ** power != len(app_cores):
            raise Exception('Core count must be power of 2')
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecFreqmine(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'freqmine'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecRaytrace(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'raytrace'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecStreamcluster(Parsec):
    # NOTE: Native takes a long time to run ~14 minutes
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'streamcluster'
        Parsec.__init__(self, environ, app_cores, client_cores, 'simlarge', nice, instance)

class ParsecSwaptions(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'swaptions'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecVips(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'vips'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

class ParsecX264(Parsec):
    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        self._bmark_name = 'x264'
        Parsec.__init__(self, environ, app_cores, client_cores, 'native', nice, instance)

