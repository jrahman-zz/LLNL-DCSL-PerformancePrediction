

import logging
import benchmarks

def load_benchmark(name, module, module_name, benchmark_name):
    bmark_module = getattr(module, module_name)
    bmark_class = getattr(bmark_module, benchmark_name)
    return bmark_class


def load_benchmarks(environ):
    logging.debug('Loading benchmarks...')

    benchmarks = {}

    for benchmark_module in environ['benchmarks'].keys():
        
        logging.debug('Loading benchmark module %s', module_name)
        module_name = 'benchmarks.' + benchmark_module.lower()
        module = None
        try:
            module = __import__(module_name)
        except Exception as e:
            logging.warning('Failed to load benchmark module %s: %s', module_name, str(e))
            break

        if not len(environ['benchmark'][benchmark_module]) == 0:
            for benchmark in environ['benchmark'][benchmark_module].keys():
                bmark_name = benchmark_module + benchmark
                
                try:
                    bmark_class = load_benchmark(module, module_name, bmark_name)
                    benchmarks[benchmark_name] = bmark_class
                except Exception as e:
                    logging.warning('Failed to load benchmark %s: %s', bmark_name, str(e)
        else:
            try:
                bmark_name = benchmark_module
            except Exception as e:
                logging.warning('Failed to load benchmark %s: %s', bmark_name, str(e))

    return benchmarks

