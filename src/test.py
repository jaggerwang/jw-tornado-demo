#!/usr/bin/env python3
from glob import glob
import importlib
import unittest
import inspect

if __name__ == "__main__":
    modules = [v[0:-3].replace("/", ".") for v in glob("pyserver/*/test.py")]
    for module in modules:
        module = importlib.import_module(module)
        for k, v in inspect.getmembers(module, inspect.isclass):
            pass
    unittest.main()
