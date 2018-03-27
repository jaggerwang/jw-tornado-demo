import os

DEBUG = os.environ.get('DEBUG', 'true').lower() in ('true', 'yes', 'y', '1')

PATH_APP = os.environ.get('PATH_APP', os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../..')))
PATH_DATA = os.environ.get('PATH_DATA', '/tmp')
PATH_LOG = os.path.join(PATH_DATA, 'log')
PATH_UPLOAD = os.path.join(PATH_DATA, 'upload')

LOGGING_LOGGER_LEVEL = os.environ.get('LOGGING_LOGGER_LEVEL', 'DEBUG')
LOGGING_HANDLER_LEVEL = os.environ.get('LOGGING_HANDLER_LEVEL', 'DEBUG')

SESSION_COOKIE_SECRET = os.environ.get(
    'SESSION_COOKIE_SECRET', '4zi7D1)uw6VJ&Iz5@924y28Z@3@M3p!H')
SESSION_EXPIRES_DAYS = int(os.environ.get('SESSION_EXPIRES_DAYS', '1'))

MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT', '27017'))
MONGODB_NAME = os.environ.get('MONGODB_NAME', 'jwApiServer')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))
