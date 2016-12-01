import os
from distutils.util import strtobool

DEBUG = strtobool(os.getenv('DEBUG', 'false'))

PROJECT_PATH = "/app"
SRC_PATH = os.path.join(PROJECT_PATH, "src")
STATIC_PATH = os.path.join(PROJECT_PATH, "static")

DATA_PATH = "/data"
LOG_PATH = DATA_PATH
UPLOAD_PATH = os.path.join(DATA_PATH, "upload")

DOMAIN_MAIN = os.getenv('DOMAIN_MAIN')
DOMAIN_STATIC = "static.{}".format(os.getenv('DOMAIN_MAIN'))
DOMAIN_API = "api.{}".format(os.getenv('DOMAIN_MAIN'))

LOGGING_HANDLER_LEVEL = os.getenv('LOGGING_HANDLER_LEVEL')
LOGGING_LOGGER_LEVEL = os.getenv('LOGGING_LOGGER_LEVEL')

SETTINGS = {
    'debug': os.getenv('DEBUG'),
    'gzip': False,
    'cookie_secret': "4zi7D1)uw6VJ&Iz5@924y28Z@3@M3p!H",
    'login_url': "/login",
    'static_path': STATIC_PATH
}

SESSION = {
    'key_prefix': "session",
    'cookie_name': "SID",
    'cookie_options': {
        'expires_days': 7
    }
}
