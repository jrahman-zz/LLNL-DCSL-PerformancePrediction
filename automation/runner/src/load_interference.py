import logging
import benchmarks

def load_thread(module, module_name, thread_name):
    """ Load a specfic interference thread class from a module """

    thread_module = getattr(module, module_name)
    thread_class = getattr(thread_module, thread_name)
    
    return thread_class

def load_interference(environ):
    """ Load interference classes from the environment dictionary """

    logging.debug('Loading interference...')

    interference = {}

    # Snapshot the environ for easier use
    threads = environ['interference']

    for thread_module in threads:
        
        logging.debug('Loading interfence module %s', thread_module)
        module_name = 'benchmarks.' + thread_module.lower()
        module = None
        try:
            module = __import__(module_name)
        except Exception as e:
            logging.warning('Failed to load interference module %s: %s', module_name, str(e))
            break

        # Collect all the thread names in this module
        # Then collect the classes at the end
        thread_names = []

        if not len(threads[thread_module]) == 0:
            for thread in threads[thread_module]:
                thread_name = thread_module + thread
                
                if not len(threads[thread_module][thread]) == 0:
                    # Sum over all the sizes for this thread type
                    for size in threads[thread_module][thread]:
                        thread_names.append(thread_name + size)
                else:
                    # Otherwise we don't have sizes
                    thread_names.append(thread_name)
                    
        else:
            # Only one benchmark in the module
            thread_name = thread_module
            thread_names.append(thread_name)

        # With our list of class names, actually get the class
        # from within the module object
        for thread_name in thread_names:
            try:
                class_name = thread_name + "Interfere"
                cls = load_thread(module, thread_module.lower(), class_name)
                interference[thread_name] = cls
            except Exception as e:
                logging.warning('Failed to load benchmark %s: %s', thread_name, str(e))

    # Add dummy interference
    import benchmarks.dummy
    dummy = benchmarks.dummy.DummyInterfere
    interference['Dummy'] = dummy

    return interference
