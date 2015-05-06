
from load_applications import load_applications
from load_environ import load_environ


if __name__ == "__main__":

    modules = ['applications.json']
    environ = load_environ('config.json', modules)
    apps = load_applications(environ)
