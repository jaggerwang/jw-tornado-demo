from pyserver.common.const import CODE_SYSTEM_ERROR


class PyserverException(Exception):

    def __init__(self, message, code=CODE_SYSTEM_ERROR):
        super().__init__(message, code)
        self.message = message
        self.code = code
