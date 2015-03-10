
import importlib
import logging
import json

def load_applications(environ):
    logging.debug('Loading applications...')
    
    applications = {}

    appconfig = environ['applications']

    for application in appconfig.keys():
        module_name = 'automation.runner.applications.' + application.lower()
        if 'subapplications' not in appconfig[application]:
            logging.debug('Loading app %s from module %s', application, module_name)
            try:
                m = __import__(module_name)
                app_module = getattr(module, application.lower())
                app_class = getattr(app_module, application)
                applications[application] = app_class
            except Exception as e:
                logging.warning('Failed to load app %s from %s: %s', application, module_name, str(e))
                raise
        else:
            module = None
            try:
                module = __import__(module_name, fromlist=appconfig[application]['subapplications'])
            except Exception as e:
                logging.warning('Failed to load app %s from %s: %s', application, module_name, str(e))
                raise
            
            for subapp in appconfig[application]['subapplications']:
                app_name = application + subapp
                try:
                    app_module = importlib.import_module(module_name)
                    app_class = getattr(app_module, app_name)
                    applications[app_name] = app_class
                except Exception as e:
                    logging.warning('Failed to load app %s from %s: %s', app_name, module_name, str(e))
                    raise

    return applications

