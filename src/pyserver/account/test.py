from pyserver.common.error import *
from pyserver.common.test import PyserverTestCase
from .service import *
from .cache import *


class TestService(PyserverTestCase):

    @property
    def user(self):
        return {
            'username': 'jaggerwang',
            'password': '123456',
            'nickname': 'jag',
            'gender': 'm',
        }

    def test_register_user(self):
        user, error = register_user(**self.user)
        self.assertIsNone(error)

    def test_edit_user(self):
        user, error = register_user(**self.user)

        nickname = 'wjj'
        user, error = edit_user(user['_id'], {'nickname': nickname})
        self.assertIsNone(error)
        self.assertEqual(user['nickname'], nickname)

    def test_user_info(self):
        user, error = register_user(**self.user)

        user = user_info(user['_id'])
        self.assertEqual(user['username'], self.user['username'])
        self.assertEqual(user['nickname'], self.user['nickname'])

    def test_user_info_by_username(self):
        register_user(**self.user)

        user = user_info_by_username(self.user['username'])
        self.assertEqual(user['username'], self.user['username'])
        self.assertEqual(user['nickname'], self.user['nickname'])

    def test_user_list(self):
        user = self.user
        register_user(**user)
        user['username'] = 'jaggerwang1'
        user['nickname'] = 'jag1'
        register_user(**user)
        user['username'] = 'jaggerwang2'
        user['nickname'] = 'jag2'
        register_user(**user)

        users, total = user_list(limit=1)
        self.assertEqual(len(users), 1)
        self.assertEqual(total, 3)

    def test_verify_password(self):
        register_user(**self.user)

        user, error = verify_password(self.user['username'], '')
        self.assertIsNotNone(error)

        user, error = verify_password(
            self.user['username'], self.user['password']
        )
        self.assertIsNone(error)
