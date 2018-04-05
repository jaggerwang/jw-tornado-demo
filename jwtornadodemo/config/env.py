import os

DEBUG = os.environ.get('DEBUG', 'true').lower() in ('true', 'yes', 'y', '1')

PATH_APP = os.environ.get('PATH_APP', os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../..')))
PATH_DATA = os.environ.get('PATH_DATA', '/tmp')
PATH_LOG = os.path.join(PATH_DATA, 'log')
PATH_UPLOAD = os.path.join(PATH_DATA, 'upload')

LOGGING_LOGGER_LEVEL = os.environ.get('LOGGING_LOGGER_LEVEL', 'DEBUG')

TORNADO_SERVER_PORT = int(os.environ.get('TORNADO_SERVER_PORT', '8888'))
TORNADO_SERVER_NUMPROCS = int(os.environ.get('TORNADO_SERVER_NUMPROCS', '0'))

SESSION_COOKIE_SECRET = os.environ.get(
    'SESSION_COOKIE_SECRET', '4zi7D1)uw6VJ&Iz5@924y28Z@3@M3p!H')
SESSION_EXPIRES_SECONDS = int(os.environ.get('SESSION_EXPIRES_SECONDS',
                                             '86400'))

MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT', '27017'))
MONGODB_NAME = os.environ.get('MONGODB_NAME', 'jw_tornado_demo')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))
