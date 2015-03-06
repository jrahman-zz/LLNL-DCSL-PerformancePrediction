from benchmark import Benchmark

import re
import logging

class Dhrystone(Benchmark):

    def __init__(self, environ, cores=[0], instance=1):
        Benchmark.__init__(self, environ, cores)
        self._cmd = self._benchmark_dir + '/dhrystone'
        self._params = []
        self._name = 'dhrystone'

    def _process_output(self, output):
        regex = r"VAX MIPS rating:\s*(\d+(?:\.\d*))"

        result = re.search(regex, output)
        if result == None:
            logging.error('Mismatch: %s', output)
            raise Exception('No match')

        features = {
                'vax_mips': float(result.group(1))
        }
        return features

if __name__ == "__main__":
    benchmark = Dhrystone({'benchmark_dir': '../../benchmarks/bin', 'data_dir': ''})
    print benchmark.run()
