from wtforms_tornado import Form
from wtforms.validators import InputRequired, Optional, AnyOf

from pylib.form.field import *
from pylib.form.validator import *

from pyserver.common.const import *
from .const import *


class UploadFileForm(Form):
    place = IntegerField(validators=[Optional(), AnyOf(PLACE_CHOICES)],
                         default=PLACE_LOCAL)


class FileInfoForm(Form):
    id = ObjectIdField(validators=[InputRequired()])
