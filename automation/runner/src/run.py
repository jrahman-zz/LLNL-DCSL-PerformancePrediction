from load_environ import load_environ
from load_applications import load_applications
from load_benchmarks import load_benchmarks
from load_interference import load_interference
import load_numa

import argparse
import logging
import json

from contexter import ExitStack

def run(applications, interference, benchmarks):
    """ Run a given set of applications in interference conditions """

    times = {}
    for application in applications:
        try:
            application.load()

            with ExitStack() as top_stack:
                for thread in interference:
                    top_stack.enter_context(thread)
                with ExitStack() as stack:
                    for thread in interference:
                        stack.enter_context(thread)
                    times[application] = {}
                    times[application]['benchmarks'] = run_benchmarks(benchmarks)
                    times[application]['application'] = run_application(application)
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
        benchmark.start()
        times[benchmark] = benchmark.get()
    return times

    
def get_args():
    parser = argparse.ArgumentParser(description='Run benchmarks and applications to collect data')
    parser.add_argument('--interference', help='Comma separated list of interfering applications and benchmarks', default='Dummy:1:1:0', type=str)
    parser.add_argument('--applications', help='Comma separated list of applications to run', default='all', type=str)
    parser.add_argument('--output', help='Output file path', default='output.json', type=str)
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
    components = interference_spec.split(':')
    print interference_spec
    name = str(components[0])
    cores = int(components[1])
    coloc_level = int(components[2])
    nice_level = int(components[3])
    return (name, cores, coloc_level, nice_level)
   
def create_config(environ, application_list, interference_specs):
    """ For a given application and interference listing, create the config """
    
    benchmarks = load_benchmarks(environ)
    interfere_threads = load_interference(environ)
    apps = load_applications(environ)

    # Parse the interference specs, and extract core request counts
    specs = map(lambda x: parse_interference(x), interference_specs)
    requests = map(lambda x: (x[1], x[2]), specs)

    # Get our core assignments from the numa detection
    (app_cores, interference_cores, client_cores) = load_numa.get_cores_new(1, requests, 1)
    
    # Set up dictionary with both apps and interfere threads
    interfere = apps.copy()
    interfere.update(interfere_threads)

    # Process threads for use
    threads = zip(specs, interference_cores, range(2, len(specs)+2)) # Specs, Cores, Instance Num
    threads = map(lambda x: (x[0][0], x[0][3], x[1], x[2]+2)) # Name,Nice,Cores,Instance
    threads = map(lambda x: interfere[x[0]](environ, x[2], client_cores, x[1], x[3]))

    # Process benchmarks for use
    benchmarks = map(lambda key: benchmarks[key](environ, app_cores), benchmarks.keys())

    applications = map(lambda key: applications[key](environ, app_cores, client_cores), application_list)

    return (applications, benchmarks, threads)
    

def main():

    args = get_args()
    interference_specs = args.interference.split(',')
    application_list = args.applications.split(',')
    output_path = args.output

    modules=['applications.json', 'benchmarks.json', 'interference.json']
    environ = load_environ('config.json', modules)
   
    logging.info('Building configuration')
    (apps, bmarks, threads) = create_config(environ, application_list, interference_specs)
    
    logging.info('Starting run')
    output = run(apps, bmarks, threads)

    with open(output_path, 'w') as f:
        json.dump(output, f)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
