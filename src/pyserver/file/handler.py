from pyserver.common.auth import authenticated
from pyserver.common.handler import PyserverHandler
from pyserver.common.const import *
from .service import *
from .form import *
from .const import *
from .vo import *


class UploadFileHandler(PyserverHandler):

    @authenticated()
    def post(self):
        form = UploadFileForm(self.request.arguments)
        if not form.validate():
            return self.response_json(CODE_PARAM_WRONG, form.errors)

        code = CODE_OK
        files = []
        for _, v in self.request.files.items():
            for u in v:
                if form.data['place'] == PLACE_LOCAL:
                    code, id = save_file_to_local(
                        u['body'], u['content_type'], filename=u['filename'],
                        uploader_id=self.current_user_id)
                else:
                    return self.response_json(CODE_PARAM_WRONG)
                files.append(file_info(id))

        self.response_json(code, files=[FileVO(v)(self) for v in files])


class FileInfoHandler(PyserverHandler):

    @authenticated()
    def get(self):
        form = FileInfoForm(self.request.arguments)
        if not form.validate():
            return self.response_json(CODE_PARAM_WRONG, form.errors)

        file = file_info(form.data['id'])

        code = CODE_OK if file else CODE_RESOURCE_NOT_FOUND
        self.response_json(code, file=FileVO(file)(self))
