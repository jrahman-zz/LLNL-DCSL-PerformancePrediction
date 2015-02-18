
import logging
import json

import gevent

from load_environ import load_environ
from load_applications import load_applications
from load_benchmarks import load_benchmarks


def main():

    submodules = ['applications.json', 'benchmarks.json']
    environ = load_environ('config.json', submodules)
    apps = load_applications(environ)
    (bmarks, threads) = load_benchmarks(environ)

    thread = threads['StreamAdd'](environ, [1, 2])

    print 'Starting interference'
    with thread:
        gevent.sleep(30)
    print 'Done with interference'

    # Core pin
    app_cores = [0]
    client_cores = [5]

    # Run over everything
    data = {}
    for app_cls in apps.values():
        app = app_cls(environ, app_cores, client_cores)
        app_name = str(app)

        # Prepare app
        print 'Loading app %s' % (app_name)
        app.load()
        
        data[app_name] = {}
        with app:
            for thread_cls in threads.values():
                # TODO, the IOBench constructors don't conform (yet)
                thread = thread_cls(environ, app_cores)
                thread_name = str(thread)
                data[app_name][thread_name] = {}
                with thread:
                    data[app_name][thread_name] = app.run()
        
        # Finish app
        print 'Cleaning up app %s' % (app_name)
        app.cleanup()

    # TODO, format the data better
    print json.dumps(data)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
