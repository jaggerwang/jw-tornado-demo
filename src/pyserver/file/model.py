from bson import ObjectId

from pyserver.common.model import get_mongo_database, PyserverMongoModel


class FileModel(PyserverMongoModel):
    _fields = {
        'place': (int, True),
        'path': (str, True),
        'size': (int, True),
        'mime': (str, False),
        'filename': (str, False),
        'uploader_id': (ObjectId, False),
    }

    def __init__(self, **kwargs):
        super().__init__(get_mongo_database("default"), "file", **kwargs)
