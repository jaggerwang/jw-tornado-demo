import code
import unittest
import sys
import readline
import rlcompleter

from cement.core import controller

from pyserver.config.main import *
from pyserver.config.db import MONGODB
from pyserver.config.cache import REDIS


class PyserverController(controller.CementBaseController):

    class Meta:
        label = 'base'
        description = 'Pyserver admin console.'
        arguments = [
            (['-t', '--test'], dict(action='store_true',
                                    help='init test environment'))
        ]

    @controller.expose()
    def default(self):
        if self.app.pargs.test:
            self._init_test_env()

        namespace = globals()
        namespace.update(locals())
        readline.set_completer(rlcompleter.Completer(namespace).complete)
        readline.parse_and_bind('tab: complete')
        code.interact(local=namespace)

    def _init_test_env(self):
        for _, configs in MONGODB.items():
            configs['name'] = 'test_{}'.format(configs['name'])

        for _, configs in REDIS.items():
            configs['db'] = 15


class TestController(PyserverController):

    class Meta:
        label = 'test'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run unittest.'
        arguments = [
            (['name'], dict(nargs='*',
                            help='name of tests to run'))
        ]

    @controller.expose()
    def default(self):
        self._init_test_env()

        loader = unittest.TestLoader()
        if len(self.app.pargs.name) == 0:
            suite = loader.discover(SRC_PATH)
        else:
            suite = unittest.TestSuite()
            for name in self.app.pargs.name:
                suite.addTest(loader.loadTestsFromName(name))

        result = unittest.TextTestRunner().run(suite)
        if not result.wasSuccessful():
            sys.exit('run test failed')
