from wtforms_tornado import Form
from wtforms.validators import InputRequired, Optional, AnyOf

from pylib.form.field import *
from pylib.form.validator import *

from pyserver.common.const import *
from .const import *


class RegisterUserForm(Form):
    username = StringField(validators=[InputRequired(), DisplayWidth(3, 20)])
    password = StringField(validators=[InputRequired(), DisplayWidth(5, 20)])
    nick = StringField(validators=[InputRequired(), DisplayWidth(2, 20)])
    gender = StringField(
        validators=[InputRequired(), AnyOf(USER_GENDER_CHOICES)])
    avatar_id = ObjectIdField(validators=[Optional()])
    intro = StringField(validators=[Optional(), DisplayWidth(2, 50)])


class EditUserForm(Form):
    nick = StringField(validators=[Optional(), DisplayWidth(2, 20)])
    gender = StringField(validators=[Optional(), AnyOf(USER_GENDER_CHOICES)])
    avatar_id = ObjectIdField(validators=[Optional()], empty_to_default=False)
    intro = StringField(validators=[Optional(), DisplayWidth(2, 50)],
                        empty_to_default=False)


class LoginForm(Form):
    username = StringField(validators=[InputRequired(), DisplayWidth(3, 50)])
    password = StringField(validators=[InputRequired(), DisplayWidth(5, 20)])
