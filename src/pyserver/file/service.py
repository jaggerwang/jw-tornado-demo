import os
import uuid
import mimetypes

from pyserver.config.main import *
from pyserver.common.const import *
from pyserver.common.exception import PyserverException
from .const import *
from .model import *


def save_file_to_local(content, mime, filename=None, uploader_id=None):
    if filename is not None:
        _, ext = os.path.splitext(filename)
    else:
        ext = mimetypes.guess_extension(mime)
    if ext is None:
        raise PyserverException("can't detecting extension")

    path = uuid.uuid4().hex + ext
    with open(os.path.join(UPLOAD_PATH, path), 'w+b') as f:
        f.write(content)

    doc = {
        'place': PLACE_LOCAL,
        'path': path,
        'size': len(content),
        'mime': mime,
        'filename': filename,
        'uploader_id': uploader_id,
    }
    id = FileModel().create(doc)

    return CODE_OK, id


def file_info(id):
    return FileModel().find_one(id)


def file_infos(ids):
    return FileModel().find_by_ids(ids, True)


def file_url(doc):
    if doc is None:
        return ""

    if doc['place'] == PLACE_LOCAL:
        url = "/upload/{}".format(doc['path'])
    else:
        url = ""

    return url
