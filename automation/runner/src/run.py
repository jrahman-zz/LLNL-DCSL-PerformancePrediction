from load_environ import load_environ
from load_applications import load_applications
from load_benchmarks import load_benchmarks

import argparse
import logging
import json

def run(
        environ,
        interference_benchmark,
        applications,
        benchmarks,
        interference,
        app_cores,
        client_cores,
        interference_cores):

    times = {}

    # Create and start interference
    threads = []
    for i in range(len(interference_cores)):
        threads.append(interference[interference_benchmark](environ, interference_cores, i + 1))
        threads[i].start()

    for benchmark in benchmarks:
        try:
            bmark = benchmarks[benchmark](environ, app_cores)
            bmark.start()
            bmark.join()
            times[str(bmark)] = bmark.value
        except Exception as e:
            logging.warning('Failed to run benchmark %s: %s', benchmark, str(e))

    #for application in applications:
    #    app = applications[application](environ, app_cores, client_cores)
    #    try:
    #        app.load()
    #        with app:
    #            output = app.run()
    #            times[app.application_name] = output
    #    except Exception as e:
    #            logging.warning('Failed to run application %s: %s', app.application_name, str(e))
    #    finally:
    #        app.cleanup()

    for i in range(len[threads]):
        # TODO, check for failure here...
        try:
            threads[i].join()
        except Exception as e:
            logging.warning('Failed to run interference thread %s: %s', str(threads[i]), str(e))

    return times

def get_args():
    parser = argparse.ArgumentParser(description='Run benchmarks and applications to collect data')
    parser.add_argument('--interference', help='Comma separated list of interfering applications and benchmarks', default='Dummy', type=str)

    parser.add_argument('--collocation', help='Collocation between inteference and applications, 0=same core(s), 1=different core(s), same socket, 2=different socket', default=1, type=int)

    return parser.parse_args()

def main():

    args = get_args()
    interference = args.interference

    modules=['applications.json', 'benchmarks.json']
    environ = load_environ('config.json', modules)

    # Load our benchmarks and applications for use
    (benchmarks, threads) = load_benchmarks(environ)
    applications = load_applications(environ)
    
    # TODO, get NUMA info here
    app_cores = [0]
    client_cores = [2]
    interference_cores = [0]

    output = run(environ,
        interference,
        applications,
        benchmarks,
        threads,
        app_cores,
        client_cores,
        interference_cores)

    with open('output.json', 'w') as f:
        json.dump(output, f)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
