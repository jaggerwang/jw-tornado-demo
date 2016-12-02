#!/usr/bin/env python3
import os
from glob import glob
import importlib
import inspect
import traceback
import logging
import logging.config
import re

from cement.core import handler, foundation
from cement.core.exc import CaughtSignal

from pyserver.common.command import PyserverController
from pyserver.config.main import *
from pyserver.config.log import LOGGING


class PyserverApp(foundation.CementApp):

    class Meta:
        label = "pyserver"
        base_controller = PyserverController


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING)

    clogger = logging.getLogger('command')

    with PyserverApp() as app:
        for module in ['.'.join(
            re.fullmatch(SRC_PATH + '/(.+)\.py', v).group(1).split('/')
        ) for v in glob(os.path.join(SRC_PATH, "pyserver/*/command.py"))]:
            module = importlib.import_module(module)
            commands = [
                v[1] for v in inspect.getmembers(module, inspect.isclass)
                if (issubclass(v[1], PyserverController) and
                    v[0] != 'PyserverController')
            ]
            for command in commands:
                handler.register(command)

        try:
            app.run()
        except CaughtSignal as e:
            clogger.info("caught signal: {}".format(e))
        except Exception:
            traceback.print_exc()
