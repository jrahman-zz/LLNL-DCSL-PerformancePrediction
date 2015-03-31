
from interference import Interference
from benchmark import Benchmark
import re
import logging

class MemoryV2Benchmark(Benchmark):

    def __init__(self, environ, operation=1, size=1024, repeat=10, cores=[0]):
        Benchmark.__init__(self, environ, cores)
        self._operation = operation
        if operation == 1:
            self._type = 'streaming'
        elif operation == 2:
            self._type = 'random'
        else:
            raise Exception('Invalid operation type')
        self._size = size / 4 # Adjust for element size
        self._repeat = repeat
        self._cmd = self._benchmark_dir + '/memoryV2'
        self._params = [str(operation), str(size), str(repeat)]
        self._name = "memoryv2_%s_%s" % (self._type, str(self._size))

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):
        regex = r"CPU = \d+ n = \d+ num_obs=(\d+)\nTime .+/memory%(operation)s: (\d*\.\d*)"
        regex = regex % {'operation': self._operation}
        result = re.search(regex, output)
        if result == None:
            logging.error('Mismatch: %s', output)
            raise Exception('No match found')
        feature = {
            'time': float(result.group(2)),
            'num_obs': float(result.group(1))
        }
        return feature

class MemoryV2Interference(Interference):

    def __init__(self, environ, operation=1, size=1024, repeat=1000, cores=[0], nice=0):
        Interference.__init__(self, environ, cores, nice)
        self._operation = operation
        if self._operation == 1:
            self._type = 'streaming'
        elif self._operation == 2:
            self._type = 'random'
        else:
            raise Exception('Invalid operation type')
        self._size = size / 4 # Adjust for element size
        self._repeat = repeat
        self._cmd = self._benchmark_dir + '/memoryV2'
        self._params = [str(operation), str(size), str(repeat)]
        self._name = 'memoryv2_%s_%s' % (self._type, str(self._size))


class MemoryV2Stream1K(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 1024, 1, cores)

class MemoryV2Stream1KInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 1, 1024, 1000, cores, nice)

class MemoryV2Stream256K(MemoryV2Benchmark):
	def __init__(self, environ, cores=[0], instance=1):
		MemoryV2Benchmark.__init__(self, environ, 1, 256 * 1024, 1, cores)

class MemoryV2Stream256KInterfere(MemoryV2Interference):
	def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
		MemoryV2Interference.__init__(self, environ, 1, 256*1024, 1000, cores, nice)

class MemoryV2Stream512K(MemoryV2Benchmark):
	def __init__(self, environ, cores=[0], instance=1):
		MemoryV2Benchmark.__init__(self, environ, 1, 512*1024, 1, cores)

class MemoryV2Stream512KInterfere(MemoryV2Interference):
	def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
		MemoryV2Interference.__init__(self, environ, 1, 512*1024, 1000, cores, nice)

class MemoryV2Stream1M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 1024 * 1024, 1, cores)

class MemoryV2Stream1MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 1, 1024 * 1024, 1000, cores, nice)

class MemoryV2Stream4M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 4*1024*1024, 1, cores)

class MemoryV2Stream4MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 1, 4*1024*1024, 1000, cores, nice)

class MemoryV2Stream8M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 8*1024*1024, 1, cores)

class MemoryV2Stream8MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 1, 8*1024*1024, 1000, cores, nice)

class MemoryV2Stream12M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 12*1024*1024, 1, cores)

class MemoryV2Stream12MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 1, 12*1024*1024, 1000, cores, nice)

class MemoryV2Stream16M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 16*1024*1024, 1, cores)

class MemoryV2Stream16MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 1, 16*1024*1024, 1000, cores, nice)

class MemoryV2Stream24M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 24*1024*1024, 1, cores)

class MemoryV2Stream24MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 1, 24*1024*1024, 1000, cores, nice)

class MemoryV2Stream32M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 32*1024*1024, 1, cores)

class MemoryV2Stream32MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 1, 32*1024*1024, 1000, cores, nice)

class MemoryV2Stream128M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 1, 1024*1024*128, 1, cores)

class MemoryV2Stream128MInterfere(MemoryV2Interference):
	def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
		MemoryV2Interference.__init__(self, environ, 1, 1024*1024*128, 1000, cores, nice)

class MemoryV2Random1K(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 2, 1024, 1, cores)

class MemoryV2Random1KInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 2, 1024, 1000, cores, nice)

class MemoryV2Random256K(MemoryV2Benchmark):
	def __init__(self, environ, cores=[0], instance=1):
		MemoryV2Benchmark.__init__(self, environ, 2, 256 * 1024, 1, cores)

class MemoryV2Random256KInterfere(MemoryV2Interference):
	def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
		MemoryV2Interference.__init__(self, environ, 2, 256*1024, 1000, cores, nice)

class MemoryV2Random512K(MemoryV2Benchmark):
	def __init__(self, environ, cores=[0], instance=1):
		MemoryV2Benchmark.__init__(self, environ, 2, 512*1024, 1, cores)

class MemoryV2Random512KInterfere(MemoryV2Interference):
	def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
		MemoryV2Interference.__init__(self, environ, 2, 512*1024, 1000, cores, nice)

class MemoryV2Random1M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 2, 1024*1024, 1, cores)

class MemoryV2Random1MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 2, 1024*1024, 1000, cores, nice)

class MemoryV2Random4M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 2, 4*1024*1024, 1, cores)

class MemoryV2Random4MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 2, 4*1024*1024, 1000, cores, nice)

class MemoryV2Random8M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 2, 8*1024*1024, 1, cores)

class MemoryV2Random8MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 2, 8*1024*1024, 1000, cores, nice)

class MemoryV2Random12M(MemoryV2Benchmark):
	def __init__(self, environ, cores=[0], instance=1):
		MemoryV2Benchmark.__init__(self, environ, 2, 12*1024*1024, 1, cores)

class MemoryV2Random12MInterfere(MemoryV2Interference):
	def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
		MemoryV2Interference.__init__(self, environ, 2, 12*1024*1024, 1000, cores)

class MemoryV2Random16M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 2, 16*1024*1024, 1, cores)

class MemoryV2Random16MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 2, 16*1024*1024, 1000, cores, nice)

class MemoryV2Random24M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 2, 24*1024*1024, 1, cores)

class MemoryV2Random24MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 2, 24*1024*1024, 1000, cores, nice)

class MemoryV2Random32M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 2, 32*1024*1024, 1, cores)

class MemoryV2Random32MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 2, 32*1024*1024, 1000, cores, nice)

class MemoryV2Random128M(MemoryV2Benchmark):
    def __init__(self, environ, cores=[0], instance=1):
        MemoryV2Benchmark.__init__(self, environ, 2, 1024*1024*128, 1, cores)

class MemoryV2Random128MInterfere(MemoryV2Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        MemoryV2Interference.__init__(self, environ, 2, 1024*1024*128, 1000, cores, nice)


if __name__ == "__main__":

    test = """./memoryV2 1 1024 100
CPU = 0 n = 1024 num_obs=976562
Time ./example1: 11.696210872"""

    benchmark = MemoryV2Stream1K({'benchmark_dir': ''})
    output = benchmark._process_output(test)

    if not output['time'] == 11.696210872:
        print 'Bad output %f, expected 11.696210872' % output['time']
        exit(1)

    if not output['num_obs'] == 976562:
        print 'Bad output %d, expected 976562' % output['num_obs']
        exit(2)

    exit(0)
