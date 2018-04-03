import os

from .env import *

APP = {
    'debug': DEBUG,
    'gzip': False,
    'cookie_secret': SESSION_COOKIE_SECRET,
    'login_url': '/login',
    'static_path': os.path.join(PATH_APP, 'static')
}
