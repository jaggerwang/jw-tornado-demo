from ..common import model


class UserModel(model.Model):
    _fields = {
        'username': (str, True),
        'password': (str, True),
        'salt': (str, True),
        'nickname': (str, True),
        'gender': (str, True),
    }

    def __init__(self, **kwargs):
        super().__init__('user', **kwargs)
