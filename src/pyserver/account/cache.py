from pyserver.common.cache import PyserverCache


class UserCache(PyserverCache):

    def __init__(self):
        super().__init__('default')
