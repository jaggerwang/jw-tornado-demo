from pyserver.common.model import get_mongo_database, PyserverMongoModel


class UserModel(PyserverMongoModel):
    _fields = {
        'username': (str, True),
        'password': (str, True),
        'salt': (str, True),
        'nickname': (str, True),
        'gender': (str, True),
    }

    def __init__(self, **kwargs):
        super().__init__(get_mongo_database('default'), 'user', **kwargs)
