

import logging
import benchmarks

def load_benchmark(module, module_name, benchmark_name):
    """ Load a specfic benchmark class from a module """

    bmark_module = getattr(module, module_name)
    bmark_class = getattr(bmark_module, benchmark_name)
    
    return bmark_class

def load_benchmarks(environ):
    """ Load benchmark classes from the environment dictionary """

    logging.debug('Loading benchmarks...')

    bmarks = {}
    interference = {}

    # Snapshot the environ for easier use
    benchmarks = environ['benchmarks']

    for bmark_module in benchmarks:
        
        logging.debug('Loading benchmark module %s', bmark_module)
        module_name = 'benchmarks.' + bmark_module.lower()
        module = None
        try:
            module = __import__(module_name)
        except Exception as e:
            logging.warning('Failed to load benchmark module %s: %s', module_name, str(e))
            break

        # Collect all the benchmark names in this module
        # Then collect the classes at the end
        bmark_names = []

        if not len(benchmarks[bmark_module]) == 0:
            for bmark in benchmarks[bmark_module]:
                bmark_name = bmark_module + bmark
                
                if not len(benchmarks[bmark_module][bmark]) == 0:
                    # Sum over all the sizes for this bmark
                    for size in benchmarks[bmark_module][bmark]:
                        bmark_names.append(bmark_name + size)
                else:
                    # Otherwise we don't have sizes
                    bmark_names.append(bmark_name)
                    
        else:
            # Only one benchmark in the module
            bmark_name = bmark_module
            bmark_names.append(bmark_name)

        # With our list of class names, actually get the class
        # from within the module object
        for bmark_name in bmark_names:
            try:
                cls = load_benchmark(module, bmark_module.lower(), bmark_name)
                bmarks[bmark_name] = cls
                thread_name = bmark_name + "Interfere"
                cls = load_benchmark(module, bmark_module.lower(), thread_name)
                interference[bmark_name] = cls
            except Exception as e:
                logging.warning('Failed to load benchmark %s: %s', bmark_name, str(e))
    
    return (bmarks, interference)
