from unittest import TestCase

from redis import StrictRedis

from pyserver.config.db import MONGODB
from pyserver.config.cache import REDIS
from pyserver.common.model import get_mongo_database


class PyserverTestCase(TestCase):

    def setUp(self):
        for alias, configs in MONGODB.items():
            db = get_mongo_database(alias)
            coll_names = db.collection_names(False)
            for coll_name in coll_names:
                coll = db[coll_name]
                coll.remove()

        for alias, configs in REDIS.items():
            db = StrictRedis(**REDIS[alias])
            db.flushdb()

    def tearDown(self):
        pass
