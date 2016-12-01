from pyserver.common.vo import PyserverVO
from .service import *


class FileVO(PyserverVO):

    def __call__(self, handler):
        vo = self._copy_mo(handler)
        if vo is None:
            return None

        vo['url'] = file_url(self.mo)

        return vo
