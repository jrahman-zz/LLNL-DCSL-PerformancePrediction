
from interference import Interference
from benchmark import Benchmark
import re
import logging

class MemoryBenchmark(Benchmark):

    def __init__(self, environ, operation=1, size=1024, repeat=10, cores=[0]):
        Benchmark.__init__(self, environ, cores)
        self._operation = operation
        if operation == 1:
            self._type = 'streaming'
        elif operation == 2:
            self._type = 'random'
        else:
            raise Exception('Invalid operation type')
        self._size = size
        self._repeat = repeat
        self._cmd = self._benchmark_dir + '/memory'
        self._params = [str(operation), str(size), str(repeat)]
        self._name = "memory_%s_%s" % (self._type, str(self._size))

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):
        regex = r"CPU = \d+ n = %(size)s num_obs=(\d+)\nTime .+/memory%(operation)s: (\d*\.\d*)"
        regex = regex % {
                    'size': self._size,
                    'repeat': self._repeat,
                    'operation': self._operation
                }
        result = re.search(regex, output)
        if result == None:
            logging.error('Mismatch: %s', output)
            raise Exception('No match found')
        feature = {
            'time': float(result.group(2)),
            'num_obs': float(result.group(1))
        }
        return feature

class MemoryInterference(Interference):

    def __init__(self, environ, operation=1, size=1024, repeat=100, cores=[0], nice=0):
        Interference.__init__(self, environ, cores, nice)
        self._operation = operation
        if self._operation == 1:
            self._type = 'streaming'
        elif self._operation == 2:
            self._type = 'random'
        else:
            raise Exception('Invalid operation type')
        self._size = size
        self._repeat = repeat
        self._cmd = self._benchmark_dir + '/memory'
        self._params = [str(operation), str(size), str(repeat)]
        self._name = 'memory_%s_%s' % (self._type, str(self._size))

class MemoryStream1K(MemoryBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryBenchmark.__init__(self, environ, 1, 1024, 10, cores)

class MemoryStream1KInterfere(MemoryInterference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryInterference.__init__(self, environ, 1, 1024, 100, cores, nice)

class MemoryStream1M(MemoryBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryBenchmark.__init__(self, environ, 1, 1024 * 1024, 10, cores)

class MemoryStream1MInterfere(MemoryInterference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryInterference.__init__(self, environ, 1, 1024 * 1024, 100, cores, nice)

class MemoryStream256M(MemoryBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryBenchmark.__init__(self, environ, 1, 1024*1024*256, 1, cores)

class MemoryStream256MInterfere(MemoryInterference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryInterference.__init__(self, environ, 1, 1024*1024*256, 10, cores, nice)

class MemoryRandom1K(MemoryBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryBenchmark.__init__(self, environ, 2, 1024, 10, cores)

class MemoryRandom1KInterfere(MemoryInterference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryInterference.__init__(self, environ, 2, 1024, 100, cores, nice)

class MemoryRandom1M(MemoryBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryBenchmark.__init__(self, environ, 2, 1024*1024, 10, cores)

class MemoryRandom1MInterfere(MemoryInterference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryInterference.__init__(self, environ, 2, 1024*1024, 100, cores, nice)

class MemoryRandom256M(MemoryBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryBenchmark.__init__(self, environ, 2, 1024*1024*256, cores)

class MemoryRandom256MInterfere(MemoryInterference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryInterference.__init__(self, environ, 2, 1024*1024*256, 10, cores, nice)


if __name__ == "__main__":

    test = """./example 1 1024 100
CPU = 0 n = 1024 num_obs=976562
Time ./example1: 11.696210872"""

    benchmark = MemoryStream1K({'benchmark_dir': ''})
    output = benchmark._process_output(test)

    if not output['time'] == 11.696210872:
        print 'Bad output %f, expected 11.696210872' % output['time']
        exit(1)

    if not output['num_obs'] == 976562:
        print 'Bad output %d, expected 976562' % output['num_obs']
        exit(2)

    exit(0)
