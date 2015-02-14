

import logging
import json
import applications

def load_applications(environ, file_path):
    logging.debug('Loading applications...')
    
    applications = {}

    for application in environ['applications'].keys():
        module_name = 'applications.' + application.lower()
        logging.debug('Loading application %s from module %s', application, module_name)
        try:
            module = __import__(module_name)
            app_class = getattr(module, application)
            instance = app_class() # TODO, need a mechanism for passing cores in
            applications[application] = instance
        except e:
            logging.warning('Failed to load application %s from %s', application, module_name)

    return applications

