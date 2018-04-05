import functools

from . import error


def authenticated():

    def _authenticated(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.current_user is None:
                return self.response_json(error.Error(
                    error.ERROR_CODE_NOT_LOGINED))

            return method(self, *args, **kwargs)
        return wrapper

    return _authenticated
