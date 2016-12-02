#!/usr/bin/env python3
from glob import glob
import importlib
import unittest
import inspect
import logging.config
import re

from pyserver.config.main import *
from pyserver.config.log import LOGGING

if __name__ == "__main__":
    logging.config.dictConfig(LOGGING)

    for module in ['.'.join(
        re.fullmatch(SRC_PATH + '/(.+)\.py', v).group(1).split('/')
    ) for v in glob(os.path.join(SRC_PATH, "pyserver/*/test.py"))]:
        module = importlib.import_module(module)
        for k, v in inspect.getmembers(module, inspect.isclass):
            pass
    unittest.main()
