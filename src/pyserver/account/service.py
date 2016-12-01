import re
import logging

from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING, DESCENDING

import pylib.security
import pylib.type
import pylib.string

from pyserver.config.main import *
from pyserver.common.const import *
from .model import *
from .cache import *
from .const import *

logger = logging.getLogger('app')


def register_user(username, password, nick, gender, avatar_id=None,
                  intro=None):
    salt = pylib.string.random_string(8)
    password = pylib.security.password_hash(password, salt)

    doc = {
        'username': username,
        'password': password,
        'salt': salt,
        'nick': nick,
        'gender': gender,
        'avatar_id': avatar_id,
        'intro': intro
    }
    try:
        id = UserModel().create(doc)
    except DuplicateKeyError:
        return CODE_RESOURCE_DUPLICATED, None

    return CODE_OK, user_info(id)


def edit_user(id, doc):
    user = UserModel().find_one(id)
    if user is None:
        return CODE_RESOURCE_NOT_FOUND

    if doc.get('password') is not None:
        doc['password'] = pylib.security.password_hash(
            doc['password'], user['salt'])

    try:
        UserModel().modify({"_id": id}, doc)
    except DuplicateKeyError:
        return CODE_RESOURCE_DUPLICATED

    return CODE_OK


def user_info(id):
    return UserModel().find_one(id)


def user_info_by_username(username):
    return UserModel().find_one({'username': username})


def user_list(keyword=None, skip=0, limit=10, sort="create_time_desc"):
    spec = {}
    if keyword is not None:
        spec['nick'] = {'$regex': r"\s*".join(re.sub(r"\s+", "", keyword)),
                        '$options': "i"}
    spec = spec or None

    s = []
    if sort == "create_time_desc":
        s.append(("create_time", DESCENDING))
    elif sort == "create_time_asc":
        s.append(("create_time", ASCENDING))
    elif sort == "nick_asc":
        s.append(("nick", ASCENDING))
    elif sort == "nick_desc":
        s.append(("nick", DESCENDING))
    s = s or None

    cursor = UserModel().find(spec, skip=skip, limit=limit, sort=s)

    return list(cursor), cursor.count()


def verify_password(username, password):
    user = UserModel().find_one({'username': username})
    if user is None:
        return CODE_RESOURCE_NOT_FOUND, None

    password = pylib.security.password_hash(password, user['salt'])
    if password == user['password']:
        return CODE_OK, user
    else:
        return CODE_USER_PASSWORD_WRONG, None
