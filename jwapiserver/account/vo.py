from ..common import vo


class UserVO(vo.VO):

    def __call__(self, handler):
        vo = self._copy_mo(handler, exclude=['password', 'salt'])
        if vo is None:
            return None

        return vo
