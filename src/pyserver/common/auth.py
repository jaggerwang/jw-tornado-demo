import functools

from pyserver.common.const import *


def authenticated():

    def _authenticated(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                return self.response_json(CODE_NOT_LOGINED)

            return method(self, *args, **kwargs)
        return wrapper

    return _authenticated
