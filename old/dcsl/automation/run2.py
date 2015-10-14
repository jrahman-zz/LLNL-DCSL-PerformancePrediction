from load_environ import load_environ
from load_applications import load_applications
from load_benchmarks import load_benchmarks
from load_interference import load_interference

import gevent
from gevent import Greenlet
import load_numa
import argparse
import math
import logging
import json

from contexter import ExitStack

def run(application, benchmarks, interference):
    """ Run a given set of applications in interference conditions """

    times = []
    try:
        application.load()

        with ExitStack() as top_stack:
            for thread in interference:
                thread.load()
                top_stack.enter_context(thread)
            with ExitStack() as stack:
                for thread in interference:
                    stack.enter_context(thread.interfere())
                try:
                    t = dict()
                    t['cores'] = application.get_cores()
                    t['application'] = str(application)
                    for i in range(0, len(interference)):
                        t['interference%d' % (i+1)] = str(interference[i])
                    t.update(run_application(application))
                    t.update(run_benchmarks(benchmarks))
                    times.append(t)
                except Exception as e:
                    logging.exception('Failed, %s', str(e)) # DEBUG
                    raise
        # Take out the trash (and there is a LOT of trash)
        for thread in interference:
                        thread.cleanup()
        application.cleanup()
    except Exception as e:
        logging.exception('Failed to run application: %s', str(application))
        raise
    return times

def run_application(application):
    """ Run the given application """
    with application:
        times = application.run()
    return times

def run_benchmarks(benchmarks):
    """ Run each selected benchmark """
    times = {}
    for benchmark in benchmarks:
        logging.info('Launching %d copies...', len(benchmark))
        greenlets = [Greenlet.spawn(lambda: bmark.run()) for bmark in benchmark]
        logging.info('Launched %d copies', len(benchmark))
        gevent.joinall(greenlets)
        results = [greenlet.value for greenlet in greenlets]

        # Perform a keywise sum across all results
        t = {}
        for res in results:
            for key in res.keys():
                if key not in t:
                    t[key] = res[key]
                else:
                    t[key] = t[key] + res[key]
        
        # Now take the arithmetic average
        for key in t.keys():
            t[key] = t[key] / len(results)

        # Merge based on keys, benchmark name first, then the type of data
        for key in t.keys():
            times["%s_%s" % (str(benchmark[0]), key)] = t[key]
    logging.debug('Done with benchmarks')
    return times

    
def get_args():
    parser = argparse.ArgumentParser(description='Run benchmarks and applications to collect data')
    parser.add_argument('--interference', help='Comma separated list of interfering applications and benchmarks', default='Dummy:1:1:0', type=str)
    parser.add_argument('--application', help='Name and core count for application to run', type=str)
    parser.add_argument('--output', help='Output file path', default='output.json', type=str)
    parser.add_argument('--config', help='Config file path', default='.', type=str)
    return parser.parse_args()


def create_interference_environment(interference_spec, environ, applications, interference):

    threads = []
    thread_specs = []
    coloc_cores = [0, 0, 0]

    for interference_thread in interference_spec.split(','):
        (interference_type, name, cores, coloc, nice) = parse_interference(interference_thread)
        thread_specs.append((interference_type, name, cores, coloc, nice))
        coloc_cores[coloc] = coloc_cores[coloc] + cores

    load_numa.get_cores

    for spec in thread_specs:
        (name, cores, coloc, nice) = thread_specs


def parse_interference(interference_spec):
    """ Break the Name:Cores:Coloc:Nice quad into a tuple """
    logging.info('Interference spec: %s', interference_spec)
    components = interference_spec.split(':')
    name = str(components[0])
    cores = int(components[1])
    coloc_level = int(components[2])
    nice_level = int(components[3])
    return (name, cores, coloc_level, nice_level)
   
def create_config(environ, application, interference_specs):
    """ For a given application and interference listing, create the config """
    
    benchmarks = load_benchmarks(environ)
    interfere_threads = load_interference(environ)
    apps = load_applications(environ)

    (application_name, application_cores) = application.split(':')
    application_cores = int(application_cores)
    
    # Parse the interference specs, and extract core request counts
    specs = map(lambda x: parse_interference(x), interference_specs)
    specs = filter(lambda x: x[0].lower() != 'dummy', specs)

    # When running multi-threaded applications, we must ensure that we have
    # interference threads evenly spread across the multi-thread application cores
    same_core_specs = filter(lambda x: x[2] == 0, specs)
    different_core_specs = filter(lambda x: x[2] != 0, specs)

    # Now replicate same core specs (Only one allowed by principle)
    if len(same_core_specs) > 1:
        raise Exception('Only one same core interference thread allowed')

    new_same_core_specs = []
    if len(same_core_specs) == 1:
        cores = int(same_core_specs[0][1])
        total = cores
        # We must have at least one interference thread
        new_same_core_specs.append(same_core_specs[0])
        for i in range(0, int(math.ceil(application_cores / cores)) - 1):
            new_same_core_specs.append(same_core_specs[0])

    # Rejoin the specs
    specs = different_core_specs + new_same_core_specs

    # (Count, Colocation)
    requests = map(lambda x: (x[1], x[2]), specs)

    # Get our core assignments from the numa detection
    (app_cores, interference_cores, client_cores) = load_numa.get_cores_new(application_cores, requests, [1])
    
    # Set up dictionary with both apps and interfere threads
    interfere = apps.copy()
    interfere.update(interfere_threads)

    # Process threads for use
    threads = zip(specs, interference_cores, range(2, len(specs)+2)) # Specs, Cores, Instance Num
    threads = map(lambda x: (x[0][0], x[0][3], x[1], x[2]), threads) # Name,Nice,Cores,Instance
    threads = map(lambda x: interfere[x[0]](environ, x[2], client_cores[0], x[1], x[3]), threads)

    # Process benchmarks for use
    bmarks = []
    for bmark in benchmarks.keys():       
        #bmarks.append([benchmarks[bmark](environ, [app_cores[i]]) for i in range(0, len(app_cores))])
		bmarks.append([benchmarks[bmark](environ, [app_cores[0]])])
    application = apps[application_name](environ, app_cores, client_cores[0], 1)
    return (application, bmarks, threads)
    
def run_experiement(interference_specs, application_list, config_path, output_path):

    modules=['applications.json', 'benchmarks.json', 'interference.json']
    modules = map(lambda x: "%s/%s" % (config_path, x), modules)
    environ = load_environ("%s/config.json" % config_path, modules)
   
    logging.info('Building configuration')
    (apps, bmarks, threads) = create_config(environ, application_list, interference_specs)
    
    logging.info('Starting run')
    output = run(apps, bmarks, threads)

    with open(output_path, 'w') as f:
        json.dump(output, f)

def main():
    args = get_args()
    interference_specs = args.interference.split(',')
    run_experiement(interference_specs, args.application, args.config, args.output)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
