
from benchmark import Benchmark
import re
import logging

class Whetstone(Benchmark):

    def __init__(self, environ, cores=[0], instance=1):
        Benchmark.__init__(self, environ, cores)
        self._cmd = self._benchmark_dir + '/whetstone'
        self._params = []
        self._name = 'whetstone'

    def _process_output(self, output):
        regex = r"Results\s*to\s*load\s*to\s*spreadsheet\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)"

        result = re.search(regex, output)
        if result == None:
            logging.error('Mismatch: %s', output)
            raise Exception('No match found')
        feature = {
                'mwips': float(result.group(1)),
                'mflops1': float(result.group(2)),
                'mflops2': float(result.group(3)),
                'mflops3': float(result.group(4)),
                'cosmops': float(result.group(5)),
                'expmops': float(result.group(6)),
                'fixpmops': float(result.group(7)),
                'ifmops': float(result.group(8)),
                'eqmops': float(result.group(9))
            }
        return feature

if __name__ == "__main__":
    benchmark = Whetstone({'benchmark_dir': '../../benchmarks/bin', 'data_dir': ''})
    print benchmark.run()
