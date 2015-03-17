from benchmark import Benchmark
from interference import Interference
import re
import logging

def str_to_num(s):
    postfix = s[-1]
    stem = s[0:-1]
    base = int(stem)
    if postfix == 'K':
        m = 1024
    elif postfix == 'M':
        m = 1024 * 1024
    elif postfix == 'G':
        m = 1024 * 1024 * 1024
    elif postfix == 'T':
        m = 1024 * 1024 * 1024 * 1024
    return base * m

class IOBenchmarkV2(Benchmark):
    """ Base class for IOBench benchmarks """

    def __init__(self, environ, cores=[0], seconds=5, read=True, size='1K', instance=1):
        Benchmark.__init__(self, environ, cores)
        self._read = read
        if read:
            self._operation = 'read'
            self._type = self._operation
        else:
            self._operation = 'writeFlush'
            self._type = 'write'
        self._size = size
        self._num_size = str_to_num(self._size)
        self._seconds = seconds
        self._path = '%s/iobench.%d' % (environ['data_dir'], instance)
        self._cmd = 'java'
        self._runstring = ','.join([self._operation, '1', self._size, self._size])
        self._params = ['-classpath', self._benchmark_dir + '/iobench.jar', 'Main', 'run', '-h=20', self._path, str(self._seconds), self._runstring]
        self._name = 'iobenchv2_%s_%s' % (self._type, self._size)

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):
        regex = r"Total for \[%s,%s,%s\]: \d+\.\d+ events \(\d+\.\d+ errors\), mean (\d*(?:\.\d*)?)ms, 10th (\d*(?:\.\d*)?)ms, 50th (\d*(?:\.\d*)?)ms, 90th (\d*(?:\.\d*)?)ms, 99th (\d*(?:\.\d*)?)ms, 999th (\d*(?:\.\d*)?)ms, 9999th (\d*(?:\.\d*)?)ms, min (\d*(?:\.\d*)?)ms, max (\d*(?:\.\d*)?)ms$"
        regex = regex % (self._operation, self._size, self._size)
        result = re.search(regex, output)
        if result == None:
            logging.error('Mismatch: %s', output)
            raise Exception('No match')

        features = {
                'mean': float(result.group(1)),
                #'p10': float(result.group(2)),
                #'p50': float(result.group(3)),
                'p90': float(result.group(4)),
                #'p99': float(result.group(5)),
                #'min': float(result.group(6)),
                #'max': float(result.group(7))
            }
        return features

class IOBenchV2Interfere(Interference):
    """ Base class for IOBench interference threads"""

    def __init__(self, environ, cores=[0], seconds=30, read=True, size='1K', nice=0, instance=1):
        Interference.__init__(self, environ, cores, nice)
        self._size = size
        self._seconds = seconds
        self._read = read
        if self._read:
            self._operation = 'read'
            self._type = self._operation
        else:
            self._operation = 'writeFlush'
            self._type = 'write'
        self._name = 'iobenchv2_%s_%s' % (self._type, '1K')
        self._path = '%s/iobench.%d' % (environ['data_dir'], instance)
        self._cmd = 'java'
        self._runstring = ','.join([self._operation, '1', self._size, self._size])
        self._params = ['-classpath', self._benchmark_dir + '/iobench.jar', 'Main', 'run', '-h=20', self._path, str(self._seconds), self._runstring]

class IOBenchV2Read1M(IOBenchmarkV2):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmarkV2.__init__(self, environ, cores, 10, True, '1M', instance)

class IOBenchV2Read1MInterfere(IOBenchV2Interfere):
    def __init__(self, environ, cores=[0],extra_cores=[1], nice=0, instance=1):
        IOBenchV2Interfere.__init__(self, environ, cores, 60, True, '1M', nice, instance)

class IOBenchV2Read4M(IOBenchmarkV2):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmarkV2.__init__(self, environ, cores, 15, True, '4M', instance)

class IOBenchV2Read4MInterfere(IOBenchV2Interfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchV2Interfere.__init__(self, environ, cores, 60, True, '4M', nice, instance)

class IOBenchV2Read128M(IOBenchmarkV2):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmarkV2.__init__(self, environ, cores, 20, True, '128M', instance)

class IOBenchV2Read128MInterfere(IOBenchV2Interfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchV2Interfere.__init__(self, environ, cores, 60, True, '128M', nice, instance)

class IOBenchV2Write1M(IOBenchmarkV2):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmarkV2.__init__(self, environ, cores, 10, False, '1M', instance)

class IOBenchV2Write1MInterfere(IOBenchV2Interfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchV2Interfere.__init__(self, environ, cores, 60, False, '1M', nice, instance)

class IOBenchV2Write4M(IOBenchmarkV2):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmarkV2.__init__(self, environ, cores, 15, False, '4M', instance)

class IOBenchV2Write4MInterfere(IOBenchV2Interfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchV2Interfere.__init__(self, environ, cores, 60, False, '4M', nice, instance)

class IOBenchV2Write128M(IOBenchmarkV2):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmarkV2.__init__(self, environ, cores, 20, False, '128M', instance)

class IOBenchV2Write128MInterfere(IOBenchV2Interfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchV2Interfere.__init__(self, environ, cores, 60, False, '128M', nice, instance)

if __name__ == '__main__':

    test = """Histogram 10 for [write,1M,1M]: 1.0 events (0.0 errors), mean 71.0ms, 10th 71.0ms, 50th 71.0ms, 90th 71.0ms, 99th 71.0ms, 999th 71.0ms, 9999th 71.0ms, min 71.0ms, max 71.0ms
Total for [write,1M,1M]: 173.0 events (0.0 errors), mean 29.8ms, 10th 5.4ms, 50th 20.8ms, 90th 62.9ms, 99th 207ms, 999th 217ms, 9999th 217ms, min 4.63ms, max 217ms"""

    m = IOBenchV2Write1M(1)
    result = m._process_output({'benchmark_dir': ''}, test)
    print result
