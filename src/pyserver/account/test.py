from bson import ObjectId

from pyserver.common.const import *
from pyserver.common.test import PyserverTestCase
from .service import *
from .cache import *


class TestService(PyserverTestCase):

    @property
    def user(self):
        return {
            'username': "jaggerwang",
            'password': "198157",
            'nick': "jag",
            'gender': "m",
        }

    def test_register_user(self):
        code, id = register_user(**self.user)
        self.assertEqual(code, CODE_OK)
        self.assertIsInstance(id, ObjectId)

    def test_edit_user(self):
        _, id = register_user(**self.user)

        nick = "wjj"
        code = edit_user(id, {'nick': nick})
        self.assertEqual(code, CODE_OK)

        user = user_info(id)
        self.assertEqual(user['nick'], nick)

    def test_user_info(self):
        _, id = register_user(**self.user)

        user = user_info(id)
        self.assertEqual(user['username'], self.user['username'])
        self.assertEqual(user['nick'], self.user['nick'])

    def test_user_info_by_username(self):
        register_user(**self.user)

        user = user_info_by_username(self.user['username'])
        self.assertEqual(user['username'], self.user['username'])
        self.assertEqual(user['nick'], self.user['nick'])

    def test_user_list(self):
        user = self.user
        register_user(**user)
        user['username'] = "jagger"
        user['nick'] = "j"
        register_user(**user)
        user['username'] = "wangjiajun"
        user['nick'] = "wjj"
        register_user(**user)

        users, total = user_list(limit=1)
        self.assertEqual(len(users), 1)
        self.assertEqual(total, 3)

    def test_verify_password(self):
        register_user(**self.user)

        code, user = verify_password(self.user['username'], "")
        self.assertEqual(code, CODE_USER_PASSWORD_WRONG)
        self.assertIsNone(user)

        code, user = verify_password(self.user['username'],
                                     self.user["password"])
        self.assertEqual(code, CODE_OK)
        self.assertIsNotNone(user)

    def test_change_password(self):
        user = self.user
        _, id = register_user(**user)

        password = "123456"
        code = change_password(id, password, user['password'])
        self.assertEqual(code, CODE_OK)

        code, user = verify_password(user['username'], password)
        self.assertEqual(code, CODE_OK)
        self.assertIsNotNone(user)
