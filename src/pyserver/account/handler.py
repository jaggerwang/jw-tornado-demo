import re

from pyserver.common.auth import authenticated
from pyserver.common.handler import PyserverHandler
from pyserver.common.const import *

from .service import *
from .form import *
from .vo import *
from .const import *


class RegisterUserHandler(PyserverHandler):

    def post(self):
        form = RegisterUserForm(self.request.arguments)
        if not form.validate():
            return self.response_json(CODE_PARAM_WRONG, form.errors)

        if not re.match(r"[a-z][a-z0-9_]{2,19}$", form.data['username'],
                        re.IGNORECASE):
            return self.response_json(CODE_PARAM_WRONG)

        code, user = register_user(**form.data)

        self.response_json(code, user=UserVO(user)(self))


class EditUserHandler(PyserverHandler):

    @authenticated()
    def post(self):
        form = EditUserForm(self.request.arguments)
        if not form.validate():
            return self.response_json(CODE_PARAM_WRONG, form.errors)

        code = edit_user(self.current_user_id, form.data)

        if code == CODE_OK:
            user = user_info(self.current_user_id)
            self.session['user'] = user

        self.response_json(code)


class AccountInfoHandler(PyserverHandler):

    @authenticated()
    def get(self):
        user = user_info(self.current_user_id)

        self.response_json(user=UserVO(user)(self))


class LoginHandler(PyserverHandler):

    def get(self):
        form = LoginForm(self.request.arguments)
        if not form.validate():
            return self.response_json(CODE_PARAM_WRONG, form.errors)

        code, user = verify_password(
            form.data['username'], form.data['password'])

        if code == CODE_OK:
            self.session['user'] = user

        self.response_json(code, user=UserVO(user)(self))


class isLoginedHandler(PyserverHandler):

    def get(self):
        user = self.session['user']

        self.response_json(user=UserVO(user)(self))


class LogoutHandler(PyserverHandler):

    def get(self):
        del self.session['user']

        self.response_json()
