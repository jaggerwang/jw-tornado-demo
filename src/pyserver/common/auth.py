import functools

from pyserver.common.error import *


def authenticated():

    def _authenticated(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                return self.response_json(Error(ERROR_CODE_NOT_LOGINED))

            return method(self, *args, **kwargs)
        return wrapper

    return _authenticated
