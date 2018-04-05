import re

import pymongo.errors
import pymongo

import pylib.security
import pylib.type
import pylib.string

from ..common import error
from .model import *
from .cache import *


def register_user(username, password, nickname, gender):
    salt = pylib.string.random_string(8)
    password = pylib.security.password_hash(password, salt)

    doc = {
        'username': username,
        'password': password,
        'salt': salt,
        'nickname': nickname,
        'gender': gender
    }
    try:
        id = UserModel().create(doc)
    except pymongo.errors.DuplicateKeyError:
        return None, error.ServiceError(error.ERROR_CODE_RESOURCE_DUPLICATED)

    return user_info(id), None


def edit_user(id, doc):
    user = UserModel().find_one(id)
    if user is None:
        return None, error.ServiceError(error.ERROR_CODE_RESOURCE_NOT_FOUND)

    if doc.get('password') is not None:
        doc['password'] = pylib.security.password_hash(
            doc['password'], user['salt'])

    try:
        UserModel().modify({'_id': id}, doc)
    except pymongo.errors.DuplicateKeyError:
        return None, error.ServiceError(error.ERROR_CODE_RESOURCE_DUPLICATED)

    return user_info(id), None


def user_info(id):
    return UserModel().find_one(id)


def user_info_by_username(username):
    return UserModel().find_one({'username': username})


def user_list(keyword=None, skip=0, limit=10, sort='create_time_desc'):
    spec = {}
    if keyword is not None:
        spec['nickname'] = {
            '$regex': r'\s*'.join(re.sub(r'\s+', '', keyword)),
            '$options': 'i'
        }
    spec = spec or None

    s = []
    if sort == 'create_time_desc':
        s.append(('create_time', pymongo.DESCENDING))
    elif sort == 'create_time_asc':
        s.append(('create_time', pymongo.ASCENDING))
    elif sort == 'nickname_asc':
        s.append(('nickname', pymongo.ASCENDING))
    elif sort == 'nickname_desc':
        s.append(('nickname', pymongo.DESCENDING))
    s = s or None

    cursor = UserModel().find(spec, skip=skip, limit=limit, sort=s)

    return list(cursor), cursor.count()


def verify_password(username, password):
    user = UserModel().find_one({'username': username})
    if user is None:
        return None, error.ServiceError(error.ERROR_CODE_RESOURCE_NOT_FOUND)

    password = pylib.security.password_hash(password, user['salt'])
    if password == user['password']:
        return user, None
    else:
        return None, error.ServiceError(error.ERROR_CODE_USER_PASSWORD_WRONG)
