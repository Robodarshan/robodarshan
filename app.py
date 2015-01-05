#!/usr/bin/python
from __future__ import unicode_literals
import os
import sys
import multiprocessing
import gunicorn.app.base
from robodarshan import wsgi
from gunicorn.six import iteritems

# hack to make sure we can load wsgi.py as a module in this class
sys.path.insert(0, os.path.dirname(__file__))

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

# Get the environment information we need to start the server
ip = os.environ['OPENSHIFT_PYTHON_IP']
port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
host_name = os.environ['OPENSHIFT_GEAR_DNS']


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % (ip, port),
        'workers': number_of_workers(),
    }
    StandaloneApplication(wsgi.application, options).run()
