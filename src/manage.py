#!/usr/bin/env python3
from glob import glob
import importlib
import inspect
import traceback
import logging

from cement.core import handler, foundation
from cement.core.exc import CaughtSignal

from pyserver.common.command import PyserverController

clogger = logging.getLogger('command')


class PyserverApp(foundation.CementApp):

    class Meta:
        label = "pyserver"
        base_controller = PyserverController


if __name__ == "__main__":
    with PyserverApp() as app:
        modules = [v[0:-3].replace("/", ".")
                   for v in glob("pyserver/*/command.py")]
        for module in modules:
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
