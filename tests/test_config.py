import unittest

from jwtornadodemo import config


class TestConfig(unittest.TestCase):

    def test_read(self):
        self.assertTrue(config.DEBUG)
