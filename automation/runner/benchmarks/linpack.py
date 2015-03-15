from benchmark import Benchmark
import logging
import re

class Linpack(Benchmark):

    def __init__(self, environ, cores=[0], instance=1):
        Benchmark.__init__(self, environ, cores)
        self._cmd = self._benchmark_dir + '/linpack'
        self._params = []
        self._name = 'linpack'

    def _process_output(self, output):
        regex = r"Double\s*Precision\s*(\d+(?:\.\d*))\s*Mflops"
        result = re.search(regex, output)
        if result == None:
            logging.error('Mismatch: %s', output)
            raise Exception('No match')
        features = {
            'mflops': float(result.group(1))
        }
        return features

if __name__ == "__main__":
    benchmark = Linpack({'benchmark_dir': '../../benchmarks/bin', 'data_dir': ''})
    print benchmark.run()
