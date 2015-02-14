

import json

def load_environ(config_path, additional_paths):
    environ = {}

    with open(config_path) as f:
        conf = json.load(f)
        environ = conf

    for path in additional_paths:
        # Yeah, don't ask how this works
        file_name = '.'.join(path.split('/')[-1].split('.')[0:-1])
        with open(path) as f:
            conf = json.load(f)
            environ[file_name] = conf

    return environ
