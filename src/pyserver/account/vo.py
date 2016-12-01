from pyserver.common.vo import PyserverVO
from pyserver.file.vo import FileVO
from pyserver.file.service import file_info


class UserVO(PyserverVO):

    def __call__(self, handler):
        vo = self._copy_mo(handler, exclude=['password', 'salt'])
        if vo is None:
            return None

        if 'avatar_id' in self.mo:
            vo['avatar'] = FileVO(file_info(self.mo['avatar_id']))

        return vo
