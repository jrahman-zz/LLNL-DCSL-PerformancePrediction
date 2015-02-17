

import logging
import json
import applications

def load_applications(environ):
    logging.debug('Loading applications...')
    
    applications = {}

    for application in environ['applications'].keys():
        module_name = 'applications.' + application.lower()
        logging.debug('Loading application %s from module %s', application, module_name)
        try:
            module = __import__(module_name)
            app_module = getattr(module, application.lower())
            app_class = getattr(app_module, application)
            applications[application] = app_class
        except Exception as e:
            logging.warning('Failed to load application %s from %s: %s', application, module_name, str(e))

    return applications

