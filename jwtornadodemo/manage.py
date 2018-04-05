#!/usr/bin/env python
import importlib
import inspect
import logging
import logging.config
import os
import re
import traceback
from glob import glob

import cement.core
import cement.core.exc

from . import config
from .common import command


class App(cement.core.foundation.CementApp):

    class Meta:
        label = 'pyserver'
        base_controller = command.Controller


if __name__ == '__main__':
    logging.config.dictConfig(config.LOGGING)

    clogger = logging.getLogger('command')

    with App() as app:
        modules = ['.'.join(re.fullmatch(config.PATH_APP + '/(.+)\.py', v)
                            .group(1).split('/'))
                   for v in glob(os.path.join(config.PATH_APP,
                                              'pyserver/*/command.py'))]
        for module in modules:
            module = importlib.import_module(module)
            commands = [
                v[1] for v in inspect.getmembers(module, inspect.isclass)
                if (issubclass(v[1], command.Controller) and
                    v[0] != 'command.Controller')
            ]
            for command in commands:
                cement.core.handler.register(command)

        try:
            app.run()
        except cement.core.exc.CaughtSignal as e:
            clogger.info('caught signal: {}'.format(e))
        except Exception:
            traceback.print_exc()
