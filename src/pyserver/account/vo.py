from pyserver.common.vo import PyserverVO


class UserVO(PyserverVO):

    def __call__(self, handler):
        vo = self._copy_mo(handler, exclude=['password', 'salt'])
        if vo is None:
            return None

        return vo
