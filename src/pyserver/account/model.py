from bson import ObjectId

from pyserver.common.model import get_mongo_database, PyserverMongoModel


class UserModel(PyserverMongoModel):
    _fields = {
        'username': (str, True),
        'password': (str, True),
        'salt': (str, True),
        'nick': (str, True),
        'gender': (str, True),
        'avatar_id': (ObjectId, False),
        'intro': (str, False),
    }

    def __init__(self, **kwargs):
        super().__init__(get_mongo_database("default"), "user", **kwargs)
