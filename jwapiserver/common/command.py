import code
import unittest
import sys
import readline
import rlcompleter

import cement.core

from .. import config


class Controller(core.controller.CementBaseController):

    class Meta:
        label = 'base'
        description = 'Admin console.'
        arguments = [
            (['-t', '--test'], dict(action='store_true',
                                    help='init test environment'))
        ]

    @core.controller.expose()
    def default(self):
        if self.app.pargs.test:
            self._init_test_env()

        namespace = globals()
        namespace.update(locals())
        readline.set_completer(rlcompleter.Completer(namespace).complete)
        readline.parse_and_bind('tab: complete')
        code.interact(local=namespace)


class TestController(Controller):

    class Meta:
        label = 'test'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run unittest.'
        arguments = [
            (['name'], dict(nargs='*',
                            help='name of tests to run'))
        ]

    @core.controller.expose()
    def default(self):
        self._init_test_env()

        loader = unittest.TestLoader()
        if len(self.app.pargs.name) == 0:
            suite = loader.discover(config.PATH_APP)
        else:
            suite = unittest.TestSuite()
            for name in self.app.pargs.name:
                suite.addTest(loader.loadTestsFromName(name))

        result = unittest.TextTestRunner().run(suite)
        if not result.wasSuccessful():
            sys.exit('run test failed')
