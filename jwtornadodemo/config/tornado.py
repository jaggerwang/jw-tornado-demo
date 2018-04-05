import os

from .env import *

TORNADO = {
    'server': {
        'port': TORNADO_SERVER_PORT,
        'numprocs': TORNADO_SERVER_NUMPROCS,
    },
    'settings': {
        'debug': DEBUG,
        'cookie_secret': SESSION_COOKIE_SECRET,
        'login_url': '/login',
        'static_path': os.path.join(PATH_APP, 'static')
    }
}
