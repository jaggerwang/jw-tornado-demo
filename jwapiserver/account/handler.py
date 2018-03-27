import json
import re

from wtforms.validators import InputRequired, Optional, AnyOf
from wtforms_tornado import Form

from pylib.form.field import StringField
from pylib.form.validator import DisplayWidth

from ..common import auth, error, handler
from .const import *
from .service import *
from .vo import *


class RegisterUserForm(Form):
    username = StringField(
        validators=[InputRequired(), DisplayWidth(3, 20)])
    password = StringField(
        validators=[InputRequired(), DisplayWidth(5, 20)])
    nickname = StringField(
        validators=[InputRequired(), DisplayWidth(2, 20)])
    gender = StringField(
        validators=[InputRequired(), AnyOf(USER_GENDER_CHOICES)])


class RegisterUserHandler(handler.Handler):

    def post(self):
        form = RegisterUserForm(self.request.arguments)
        if not form.validate():
            return self.response_json(
                Error(ERROR_CODE_PARAM_WRONG, json.dumps(form.errors))
            )

        if not re.match(r'[a-z][a-z0-9_]{2,19}$', form.data['username'],
                        re.IGNORECASE):
            return self.response_json(Error(ERROR_CODE_PARAM_WRONG))

        user, error = register_user(**form.data)
        if error:
            return self.response_json(error)

        self.response_json(user=UserVO(user)(self))


class EditUserForm(Form):
    nickname = StringField(
        validators=[Optional(), DisplayWidth(2, 20)])
    gender = StringField(
        validators=[Optional(), AnyOf(USER_GENDER_CHOICES)])


class EditUserHandler(handler.Handler):

    @auth.authenticated()
    def post(self):
        form = EditUserForm(self.request.arguments)
        if not form.validate():
            return self.response_json(
                Error(ERROR_CODE_PARAM_WRONG, json.dumps(form.errors))
            )

        user, error = edit_user(self.current_user_id, form.data)
        if error:
            return self.response_json(error)

        self.session['user'] = user

        self.response_json(user=UserVO(user)(self))


class AccountInfoHandler(handler.Handler):

    @auth.authenticated()
    def get(self):
        user = user_info(self.current_user_id)

        self.response_json(user=UserVO(user)(self))


class LoginForm(Form):
    username = StringField(
        validators=[InputRequired(), DisplayWidth(3, 50)])
    password = StringField(
        validators=[InputRequired(), DisplayWidth(5, 20)])


class LoginHandler(handler.Handler):

    def get(self):
        form = LoginForm(self.request.arguments)
        if not form.validate():
            return self.response_json(
                Error(ERROR_CODE_PARAM_WRONG, json.dumps(form.errors))
            )

        user, error = verify_password(
            form.data['username'], form.data['password']
        )
        if error:
            return self.response_json(error)

        self.session['user'] = user

        self.response_json(user=UserVO(user)(self))


class IsLoginedHandler(handler.Handler):

    def get(self):
        user = self.session['user']

        self.response_json(user=UserVO(user)(self))


class LogoutHandler(handler.Handler):

    def get(self):
        del self.session['user']

        self.response_json()
